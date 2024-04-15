from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import fitz  
import base64
import requests
from django.core.files.base import ContentFile
# FreeImage.host API endpoint for image upload
API_KEY = '6d207e02198a847aa98d0a2a901485a5'
UPLOAD_URL = 'https://freeimage.host/api/1/upload'

@api_view(['POST'])
def extract_pdf_data(request):
    if 'pdf_file' not in request.FILES:
        return Response({'error': 'PDF file not found in request'}, status=400)
    
    # Process the uploaded PDF file
    pdf_file = request.FILES['pdf_file']
    pdf_content = ContentFile(pdf_file.read())

    text, images = extract_text_and_images_from_content(pdf_content)
    
    print("Extracted images:", images)
    try:
        image_urls = upload_to_freeimage(images)
    except Exception as e:
        print(e)
        return Response({'error': 'Failed to upload images'}, status=500)
    print("Uploaded image URLs:", image_urls)
  
    return Response({'text': text, 'image_urls': image_urls})

def extract_text_and_images_from_content(pdf_content):
    doc = fitz.open(stream=pdf_content.read(), filetype='pdf')
    text = ""
    images = []
    processed_images = set()  # To track already processed images

    for page in doc:
        text += page.get_text()
        image_list = page.get_images(full=True)
        
        if image_list:
            print("Images found on page:", len(image_list)) 

        for img_id in image_list:
            if img_id[0] in processed_images:
                continue  # Skip if this image was already processed
            processed_images.add(img_id[0])  # Mark as processed
            
            base_image = doc.extract_image(img_id[0])
            image_bytes = base_image["image"]
            images.append(image_bytes)

    return text, images

def upload_to_freeimage(images):
    image_urls = []
    
    for image in images:
        response = upload_image_to_freeimage(image)
        if 'error' in response:
            image_urls.append(None)  # Handle failure, maybe log the error
        else:
            image_url = response.get('image', {}).get('url')
            image_urls.append(image_url)
    return image_urls


def upload_image_to_freeimage(image_data):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    # Check if the image_data is already a base64 string or needs encoding
    base64_image = base64.b64encode(image_data).decode('utf-8')

    data = {
        'key': API_KEY,
        'source': base64_image,
        'format': 'json'
    }
    response = requests.post(UPLOAD_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()  # Successfully uploaded
    else:
        print('Upload failed:', response.text)
        # Ensure you return a structured response even in case of failure
        return {'error': 'Failed to upload image', 'status_code': response.status_code}
    
    
    


@api_view(['POST'])
def image_to_url(request):
    if 'image_file' not in request.FILES:
        return Response({'error': 'Image file not found in request'}, status=400)
    
    try:
        image_file = request.FILES['image_file']
        image_data = image_file.read()

        hosted_url = upload_image(image_data)
        
        return Response({'hosted_url': hosted_url})
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def upload_image(image_data):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    
    base64_image = base64.b64encode(image_data).decode('utf-8')

    data = {
        'key': API_KEY,
        'source': base64_image,
        'format': 'json'
    }

    response = requests.post(UPLOAD_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get('image', {}).get('url')
    else:
        raise Exception(f"Failed to upload image: {response.text}")       
    


