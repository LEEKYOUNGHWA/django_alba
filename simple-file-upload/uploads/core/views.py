from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm


def home(request):
    documents = Document.objects.all()
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/mainpage.html', {'uploaded_file_url': uploaded_file_url , 'documents': documents })
    if request.method == 'POST' and request.FILES['select']:
        select = request.FILES['select']
        fs = FileSystemStorage()
        select_file_url = fs.url(select.name)
        return render(request, 'core/mainpage.html', {'select_file_url': select_file_url , 'documents': documents })
    return render(request, 'core/mainpage.html', { 'documents': documents })

def contact(request):
    return render(request, 'core/contact.html', {})

def model_form_upload(request):
    documents = Document.objects.all()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = DocumentForm()
    return render(request, 'core/uploadpage.html', {'form': form , 'documents': documents })

