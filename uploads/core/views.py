from django.shortcuts import render, redirect

from uploads.core.models import SampleFacialDocument
from uploads.core.forms import InputFacialDocumentForm
from uploads.core.models import SampleWDefectDocument
from uploads.core.forms import InputWDefectDocumentForm

from uploads.core.homepage_demo.demo import FacialLandmark
from uploads.core.homepage_demo.demo import WeldingDefect
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def home(request):
    documents = SampleFacialDocument.objects.all()
    if request.method == 'POST':
        form = InputFacialDocumentForm(request.POST, request.FILES)
        # user input file save
        if form.is_valid():
            newone = form.save()
            uploaded_file_url = "/media/"+newone.idocument.name
            return render(request, 'core/mainpage.html', { 'select_file_url': uploaded_file_url,'documents': documents})
    return render(request, 'core/mainpage.html',{'documents': documents})

@xframe_options_exempt
def wfunction(request):
    documents = SampleWDefectDocument.objects.all()
    if request.method == 'POST':
        form = InputWDefectDocumentForm(request.POST, request.FILES)
        # user input file save
        if form.is_valid():
            newone = form.save()
            uploaded_file_url = "/media/" + newone.idocument.name
            return render(request, 'core/welding_defect.html', {'select_file_url': uploaded_file_url, 'documents': documents})
    return render(request, 'core/welding_defect.html', {'documents': documents})

@xframe_options_exempt
def facialfunction(request):
    documents = SampleFacialDocument.objects.all()
    if request.method == 'POST':
        url = request.POST.get("himgurl")
        if url:
            facial_landmark_url= FacialLandmark(url,url[7:])
	    #facial_landmark_url = url
            return render(request,'core/mainpage.html',{'select_file_url': facial_landmark_url,'documents':documents})
    return render(request, 'core/mainpage.html', {'documents': documents})

@xframe_options_exempt
def welding_defect(request):
    documents = SampleWDefectDocument.objects.all()
    if request.method == 'POST':
        url = request.POST.get("himgurl")
        if url:
            welding_defect_url= WeldingDefect(url,url[7:])
	    #facial_landmark_url = url
            return render(request,'core/welding_defect.html',{'select_file_url': welding_defect_url,'documents':documents})
    return render(request, 'core/welding_defect.html', {'documents': documents})