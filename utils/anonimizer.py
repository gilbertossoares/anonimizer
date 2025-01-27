import fitz  # PyMuPDF
import os
from io import BytesIO
from dotenv import load_dotenv
import tempfile
import time
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import pandas as pd
from PIL import Image, ImageDraw
import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials


if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()



form_recognizer_key = os.getenv('AZURE_FORM_RECOGNIZER_KEY')
form_recognizer_endpoint = os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT')
text_analytics_key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
text_analytics_endpoint = os.getenv('AZURE_TEXT_ANALYTCIS_ENDPOINT')
subscription_key = os.getenv("AZURE_COMPUTER_VISION_KEY")
endpoint = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")
model_id = os.getenv("AZURE_DOCUMENT_MODEL_ID")



document_analysis_client = DocumentAnalysisClient(endpoint=form_recognizer_endpoint, credential=AzureKeyCredential(form_recognizer_key))


text_analytics_client = TextAnalyticsClient(endpoint=text_analytics_endpoint, credential=AzureKeyCredential(text_analytics_key))


computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


def detect_objects(image_path):
    with open(image_path, 'rb') as image:
        detect_objects_results = computervision_client.detect_objects_in_stream(image)
        return detect_objects_results.objects
    

def draw_rectangles(image_path, detected_objects):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image, 'RGBA')

    people_detected = [obj for obj in detected_objects if obj.object_property == "person"]

    if not people_detected:
        
        return image_path

    for person in people_detected:
        rect = person.rectangle
        left = rect.x
        top = rect.y
        right = left + rect.w
        bottom = top + rect.h

        
        draw.rectangle(((left, top), (right, bottom)), fill="black")

    
    file_path, file_extension = os.path.splitext(image_path)
    output_image_path = image_path
    image.save(output_image_path)
    return output_image_path




def processar_arquivo(caminho_arquivo, output_folder, timestamp):    

    file_path = caminho_arquivo
    with open(file_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f)

    
    document = poller.result()
    
    extracted_text = ""
    for page in document.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"

    documents = [extracted_text]
    response = text_analytics_client.recognize_pii_entities(documents, language="pt-br")

    
    data = []

    
    for idx, document in enumerate(response):
        if not document.is_error:
            for entity in document.entities:
                if entity.confidence_score >= 0.1:
                    data.append({
                        "text": entity.text,
                        "category": entity.category,
                        "confidence_score": entity.confidence_score
                    })

    
    df = pd.DataFrame(data)
    
    if df.empty:
        
        detected_objects = detect_objects(file_path)

        
        output_image_path = draw_rectangles(file_path, detected_objects)

        
        base_name = os.path.splitext(os.path.basename(caminho_arquivo))[0]
        anonymized_file_path = os.path.join(output_folder, f"{base_name}_{timestamp}_anonimizado.png")
        image_pil.save(anonymized_file_path, format='PNG')
        
        return anonymized_file_path 
    else:   
        df_filtered = df[df['category'].isin(["PhoneNumber","Person","PersonType","Email","IPAddress","CreditCardNumber","Address","BRLegalEntityNumber","BRCPFNumber","BRNationalIDRG"])]
        texts_to_censor = df_filtered.values.flatten()
        texts_to_censor = [str(text).strip() for text in texts_to_censor if str(text).strip()]

        
        with open(caminho_arquivo, "rb") as image_stream:
            image_data = image_stream.read()

        
        ocr_result = computervision_client.read_in_stream(BytesIO(image_data), language="pt", raw=True,)
        operation_location_remote = ocr_result.headers["Operation-Location"]
        operation_id = operation_location_remote.split("/")[-1]

        
        import time
        while True:
            get_text_results = computervision_client.get_read_result(operation_id)
            if get_text_results.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        
        image_pil = Image.open(BytesIO(image_data))
        draw = ImageDraw.Draw(image_pil)

        
        if get_text_results.status == 'succeeded':
            read_results = get_text_results.analyze_result.read_results
            for read_result in read_results:
                for line in read_result.lines:
                    line_text = line.text
                    if any(text in line_text for text in texts_to_censor):
                        
                        x_coords = line.bounding_box[0::2]  
                        y_coords = line.bounding_box[1::2] 
                        x_min = min(x_coords)
                        y_min = min(y_coords)
                        x_max = max(x_coords)
                        y_max = max(y_coords)
                        
                        draw.rectangle([x_min, y_min, x_max, y_max], fill="black")

        
        file_path, file_extension = os.path.splitext(caminho_arquivo)
        censored_image_path = f"{file_path}_censurada_p{file_extension}"
        
        image_pil.save(censored_image_path, format='PNG')
        

        
        detected_objects = detect_objects(censored_image_path)

        
        output_image_path = draw_rectangles(censored_image_path, detected_objects)

        
        base_name = os.path.splitext(os.path.basename(caminho_arquivo))[0]
        anonymized_file_path = os.path.join(output_folder, f"{base_name}_{timestamp}_anonimizado.png")
        image_pil.save(anonymized_file_path, format='PNG')

        return anonymized_file_path 



