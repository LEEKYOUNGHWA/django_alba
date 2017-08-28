from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm
from django.http import Http404

def home(request):
    documents = Document.objects.all()
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/mainpage.html', {'uploaded_file_url': uploaded_file_url , 'documents': documents })
    return render(request, 'core/mainpage.html', { 'documents': documents })

def select(request, document_id):
    documents = Document.objects.all()
    try:
         pickd = Document.objects.get(pk=document_id)
         select_file_url = pickd.document.url
    except Document.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'core/mainpage.html', { 'documents': documents ,'select_file_url':select_file_url })

def contact(request):
    return render(request, 'core/contact.html', {})

"""
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

"""