import os
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw


if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()
    

PREDICTION_KEY = os.getenv('AZURE_CUSTOM_COMPUTE_VISION_PREDICTION_KEY')
CONTENT_TYPE = 'application/octet-stream'
API_URL = os.getenv('AZURE_CUSTOM_COMPUTE_VISION_ENDPOINT')


def analyze_image(image_path):
    with open(image_path, 'rb') as image_file:
        headers = {
            'Prediction-Key': PREDICTION_KEY,
            'Content-Type': CONTENT_TYPE,
        }
        response = requests.post(API_URL, headers=headers, data=image_file)
        response.raise_for_status()  
        return response.json()


def draw_bounding_boxes(image_path, bounding_boxes, output_folder, timestamp):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img, 'RGBA')
        for bbox in bounding_boxes:
            left = bbox['left'] * img.width
            top = bbox['top'] * img.height
            width = bbox['width'] * img.width
            height = bbox['height'] * img.height
            draw.rectangle([left, top, left + width, top + height], fill="black")

        
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}.png")
        img.save(output_path, format='PNG')
        print(f"Imagem anonimizada salva em: {output_path}")

        return output_path


def anonymize_signatures(image_path, output_folder, timestamp):
    print(f"Anonimizando assinaturas na imagem: {image_path}")
    
    
    try:
        result = analyze_image(image_path)
        
        bounding_boxes = [pred['boundingBox'] for pred in result['predictions'] if pred['probability'] > 0.10]
        
        if not bounding_boxes:
            print("Nenhuma assinatura detectada para anonimizar.")
            return image_path  
        
        
        anonymized_file_path = draw_bounding_boxes(image_path, bounding_boxes, output_folder, timestamp)
        
        return anonymized_file_path

    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar analisar a imagem: {e}")
        return None
