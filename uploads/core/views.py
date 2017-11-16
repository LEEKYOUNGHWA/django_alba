from django.shortcuts import render, redirect

from uploads.core.models import Document
from uploads.core.forms import DocumentForm
from uploads.core.forms import InputDocumentForm
from uploads.core.facial_landmarks_detection_demo.facial_landmarks_detection_demo.demo import FacialLandmark
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def home(request):
    documents = Document.objects.all()
    if request.method == 'POST':
        form = InputDocumentForm(request.POST, request.FILES)
        # user input file save
        if form.is_valid():
            form.save()
            myfile = request.FILES['idocument']
            uploaded_file_url = "/media/userinputs/"+myfile.name
            print(uploaded_file_url)
            return render(request, 'core/mainpage.html', { 'select_file_url': uploaded_file_url,'documents': documents})
    return render(request, 'core/mainpage.html',{'documents': documents})

@xframe_options_exempt
def facialfunction(request):
    documents = Document.objects.all()
    if request.method == 'POST':
        url = request.POST.get("himgurl")
        if url:
            facial_landmark_url= FacialLandmark(url,url[7:])
	    #facial_landmark_url = url
            return render(request,'core/mainpage.html',{'select_file_url': facial_landmark_url,'documents':documents})
    return render(request, 'core/mainpage.html', {'documents': documents})

@xframe_options_exempt
def contact(request):
    return render(request, 'core/contact.html', {})

@xframe_options_exempt
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
