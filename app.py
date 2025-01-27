from flask import Flask, request, render_template, send_file, jsonify
from utils.azure_blob import AzureBlobService
import os
import tempfile
from datetime import datetime
from utils.converter import converter_arquivos  
from utils.anonimizer import processar_arquivo  
from utils.signature import anonymize_signatures  
from PIL import Image, ImageDraw
import io
import json
import urllib.parse
from azure.storage.blob import BlobServiceClient
import requests
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta



app = Flask(__name__)


azure_blob_service = AzureBlobService(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
container_name = os.getenv('OUTPUT_CONTAINER_NAME')
AZURE_SEARCH_API_KEY = os.getenv('AZURE_AI_SEARCH_KEY')  
AZURE_SEARCH_ENDPOINT = os.getenv('AZURE_AI_SEARCH_ENDPOINT')
AZURE_BLOB = os.getenv('AZURE_DATALAKE_ACCOUNT_NAME')
PUBLIC_CONTAINER_URL = f'https://{AZURE_BLOB}.blob.core.windows.net/{container_name}'  


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search/query', methods=['POST'])
def search_query():
    query = request.json.get('query')
    order_by = request.json.get('orderBy', 'metadata_storage_name')
    order_direction = request.json.get('orderDirection', 'asc')
    page = request.json.get('page', 1)  
    per_page = request.json.get('perPage', 10)  
    
    headers = {
        'Content-Type': 'application/json',
        'api-key': AZURE_SEARCH_API_KEY
    }
    
    
    skip = (page - 1) * per_page
    
    
    search_url = f'{AZURE_SEARCH_ENDPOINT}&search={query}&$orderby={order_by} {order_direction}&$skip={skip}&$top={per_page}&$count=true'
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        search_results = response.json()
        total_count = search_results.get('@odata.count', 0)

        
        for result in search_results['value']:
            blob_name = result.get('metadata_storage_name')
            if blob_name:
                result['image_url'] = f"{PUBLIC_CONTAINER_URL}/{blob_name}"

        return jsonify({
            'results': search_results['value'],
            'total': total_count,
            'page': page,
            'per_page': per_page
        })
    else:
        return jsonify({'error': 'Error during search request'}), response.status_code

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    message = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            
            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir, file.filename)
            file.save(temp_file_path)

            
            png_files = []
            anonymized_files = []
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name, file_extension = os.path.splitext(file.filename)
            new_file_name = f"{file_name}_{timestamp}{file_extension}"

            container_name_input = os.getenv('INPUT_CONTAINER_NAME')
            container_name_output = os.getenv('OUTPUT_CONTAINER_NAME')

            try:
                
                azure_blob_service.upload_file(container_name_input, new_file_name, temp_file_path)

                
                png_files = converter_arquivos(temp_file_path)

                
                anonymized_files = []
                for png_file in png_files:
                    
                    anonymized_file_path = processar_arquivo(png_file, output_folder=temp_dir, timestamp=timestamp)
                    
                    signed_anonymized_file = anonymize_signatures(anonymized_file_path, output_folder=temp_dir, timestamp=timestamp)
                    anonymized_files.append(signed_anonymized_file)

                
                for anonymized_file in anonymized_files:
                    anonymized_file_name = os.path.basename(anonymized_file)
                    azure_blob_service.upload_file(container_name_output, anonymized_file_name, anonymized_file)

                
                message = f"Upload realizado com sucesso e imagens anonimizadas salvas no container de output."

            except Exception as e:
                message = f"Erro ao processar o arquivo: {str(e)}"

            
            
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
            for png_file in png_files:
                if png_file and os.path.exists(png_file):
                    os.remove(png_file)
            for anonymized_file in anonymized_files:
                if anonymized_file and os.path.exists(anonymized_file):
                    os.remove(anonymized_file)

    return render_template('upload.html', message=message)

@app.route('/modify')
def modify():
    return render_template('modify.html')

blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

@app.route('/image/<image_name>', methods=['GET'])
def load_image(image_name):
    try:
        
        image_name = urllib.parse.unquote(image_name)
        print(f"Tentando carregar a imagem: {image_name}")

        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=image_name)
        
        if not blob_client.exists():
            return f"Erro: o arquivo '{image_name}' não existe no container.", 404

        
        download_stream = blob_client.download_blob()
        image_data = download_stream.readall()

        
        temp_dir = tempfile.gettempdir()
        temp_image_path = os.path.join(temp_dir, "temp_image.png")

        with open(temp_image_path, 'wb') as f:
            f.write(image_data)
        print(f"Imagem carregada com sucesso e salva temporariamente em: {temp_image_path}")

        return send_file(temp_image_path, mimetype='image/png')

    except Exception as e:
        error_message = f"Erro ao tentar carregar a imagem: {str(e)}"
        print(error_message)
        return error_message, 500

@app.route('/save', methods=['POST'])
def save_image():
    try:
        data = request.get_json()
        image_name = data['filename']
        rectangles = data['rectangles']

        
        image_name = urllib.parse.unquote(image_name)
        print(f"Tentando salvar a imagem: {image_name}")

        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=image_name)
        
        if not blob_client.exists():
            return jsonify({"status": "error", "message": f"O arquivo '{image_name}' não existe no container."}), 404

        download_stream = blob_client.download_blob()
        image_data = download_stream.readall()

        
        image = Image.open(io.BytesIO(image_data))
        draw = ImageDraw.Draw(image)

        
        for rect in rectangles:
            x0, y0, x1, y1 = rect
            draw.rectangle([x0, y0, x1, y1],fill=(0, 0, 0, 1), outline="yellow", width=2)

        
        output = io.BytesIO()
        image.save(output, format='PNG')
        output.seek(0)

        
        blob_client.upload_blob(output, overwrite=True)

        print(f"Imagem salva com sucesso no Azure Storage: {image_name}")
        return jsonify({"status": "success"})

    except Exception as e:
        error_message = f"Erro ao tentar salvar a imagem: {str(e)}"
        print(error_message)
        return jsonify({"status": "error", "message": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)