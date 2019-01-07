from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from upload.models import Document
from upload.forms import DocumentForm
from static.script.script import *
import string

def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            documents = Document.objects.last()             # 가장 최근에 삽입한 오브젝트 로드
            createAndInsert(documents.document)             # 테이블 생성 및 튜플 삽입

            return redirect('form_upload.html')
    else:
        form = DocumentForm()
    return render(request, 'form_upload.html', {'form': form})


#####################################################################
#####################################################################
def upload(req):
    print("????????????")
    if req.method == 'POST':
        if 'file' in req.FILES:
            file = req.FILES['file']
            filename = file._name

            fp = open('%s/%s' % (UPLOAD_DIR, filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
            return HttpResponse('File Uploaded')
    return HttpResponse('Failed to Upload File')



#####################################################################
#### CBV File View
#####################################################################
from django.views.generic import View
from django.urls import reverse_lazy

class FileUploadView(View):
    form_class = DocumentForm               # form 클래스 설정
    success_url = reverse_lazy('upload')    # 성공시 'upload'라는 alias를 갖는 url로 이동
    template_name = 'form_upload.html' 

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES, auto_id=False)

        if form.is_valid():
            form.save()
            documents = Document.objects.last()
            createAndInsert(documents.document)     # document를 추가하는 비지니스로직 수행
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})