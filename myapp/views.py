# myapp/views.py

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import sys
import os

# Pythonプロジェクトのパスを追加
sys.path.append(os.path.join(settings.BASE_DIR, '..', 'image_processing'))
from image_processing import image_processing

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)
        return redirect('result') + f'?image_url={image_url}'
    return render(request, 'upload_image.html')

def result(request):
    image_url = request.GET.get('image_url')
    if image_url:
        fs = FileSystemStorage()
        image_path = fs.path(image_url)
        extracted_text = image_processing.extract_text_from_image(image_path)
        return render(request, 'result.html', {'extracted_text': extracted_text, 'image_url': image_url})
    return redirect('upload_image')
