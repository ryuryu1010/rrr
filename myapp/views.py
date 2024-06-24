# views.py
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from image_processing import extract_text_from_image  # インポート文
from django.core.exceptions import SuspiciousFileOperation

# 画像アップロード機能の関数
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)
        return redirect('result') + f'?image_url={filename}'
    return render(request, 'upload_image.html')

# 結果表示の関数
def result(request):
    image_url = request.GET.get('image_url')
    if image_url:
        fs = FileSystemStorage()
        try:
            image_path = fs.path(image_url)
            extracted_text = extract_text_from_image(image_path)
            return render(request, 'result.html', {'extracted_text': extracted_text, 'image_url': fs.url(image_url)})
        except SuspiciousFileOperation:
            # 不審なファイル操作の例外処理
            return redirect('upload_image')
    return redirect('upload_image')
