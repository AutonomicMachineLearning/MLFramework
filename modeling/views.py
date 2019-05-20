"""
from django.views.generic import ListView, DetailView, TemplateView
from modeling.models import ModelingData
"""
from django.views.generic import ListView, DetailView, TemplateView
from modeling.models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from modeling.models import Document
from static.script.script import *
from django.template import RequestContext, loader, Context
from django.http import HttpResponse
import json
from modeling.forms import DocumentForm

"""
class ModelingView_data(ListView):
    model = Table                               # 모델 설정
    template_name = "data.html"
"""

# class ModelingView_model(ListView):
#     model = Table                               # 모델 설정
#     template_name = "model.html"

class ModelingView_hyperparameter(ListView):
    model = Table                               # 모델 설정
    template_name = "hyperparameter.html"

class ModelingView_Training(ListView):
    model = Table                               # 모델 설정
    template_name = "Training.html"

class ModelingView_Result(ListView):
    model = Table                               # 모델 설정
    template_name = "result.html"

class ModelingView_Inference(ListView):
    model = Table                               # 모델 설정
    template_name = "inference.html"





class ModelingView_data(ListView):
    model = Table                               # 모델 설정
    context_object_name = 'table'               # 컨텍스트 객체 이름 지정
    template_name = "data.html"                 # 템플릿 파일 지정

    def get_context_data(self, **kwargs):
        context = super(ModelingView_data, self).get_context_data(**kwargs)

        ############### upload_document 테이블로부터 업로드된 dataset list를 불러온다.
        selectedList = selectDataListName("upload_document")
        datasetList = getDatasetNameFromList(selectedList)
        print(datasetList)

        context['datasetList'] = datasetList              # 데이터셋 리스트 저장

        # print(temp)
        ############### 테이블로부터 object를 가져온다(.csv)
        # documents = Document.objects.last()             # 가장 최근 삽입된 파일을 불러온다.
        # tableName = getTableName(documents.document)    # 파일경로로부터 테이블 이름을 추출
        # csvTable = selectData(tableName)                # 튜플 select
        # column = getColumnName(tableName)               # 컬럼명 추출

        # context['column'] = column              # 컬럼명 저장
        # context['csvTable'] = csvTable          # 튜플목록 저장

        return context


##### Ajax --- Combo Box
# def getDatasetList(request):
#     data = request.POST.get('data1')
#     print(data)
#     name = "helloworld"
#     print(name)


#     #value = RequestContext(request, {'name':name})
#     template = loader.get_template('data.html')

#     documents = Document.objects.last()             # 가장 최근 삽입된 파일을 불러온다.
#     tableName = getTableName(documents.document)    # 파일경로로부터 테이블 이름을 추출
#     csvTable = selectData(tableName)                # 튜플 select
#     column = getColumnName(tableName)               # 컬럼명 추출

#     context = {'name': name,
#                'csvTable': csvTable,
#                'column': column }

#     return HttpResponse(json.dumps(context), content_type="application/json")


##### Ajax --- Table
# def getTable_(request):
#     tableName = request.POST.get('dataSet')
#     print(tableName)

#     template = loader.get_template('data.html')     # response 템플릿 지정

#     documents = Document.objects.last()             # 가장 최근 삽입된 파일을 불러온다.
#     tableName = getTableName(documents.document)    # 파일경로로부터 테이블 이름을 추출
#     csvTable = selectData(tableName)                # 튜플 select
#     column = getColumnName(tableName)               # 컬럼명 추출

#     context = {'tableName': tableName,
#                'tuples': csvTable,
#                'column': column }

#     return HttpResponse(json.dumps(context), content_type="application/json")

############################################################################
############################################################################
############################################################################
##### Ajax --- Table
def getTable(request):
    tableName = request.POST.get('dataSet')
    print(tableName)

    template = loader.get_template('data.html')     # response 템플릿 지정

    #documents = Document.objects.last()             # 가장 최근 삽입된 파일을 불러온다.
    #tableName = getTableName(documents.document)    # 파일경로로부터 테이블 이름을 추출
    csvTable = selectData(tableName)                 # 튜플 select
    if csvTable is not None:
        column = getColumnName(tableName)               # 컬럼명 추출

    else:
        column = None

    print(csvTable)

    context = {'tableName': tableName,
               'tuples': csvTable,
               'column': column }

    return HttpResponse(json.dumps(context), content_type="application/json")
############################################################################
############################################################################
############################################################################
import ast

def setModelSequence(request):
    sequence = request.POST.get('sequence')
    sequence_json = ast.literal_eval(sequence)      # string 형태를 dictionary객체로 변환
    # print(test.get('op_0'))
    # print(test.get('op_0').get('operator_title'))
    # print(test.get('op_0').keys())

    print(json.dumps(sequence_json, ensure_ascii=False, indent="\t") )


    ############### .txt 형식으로 json 객체(딕셔너리)를 저장한다 --> /static/files/ + 프로젝트id_models.txt
    projectId = "2"         # 프로젝트 ID --> 자동생성 해야 함
    fileName = projectId + "_models.txt"    # 저장할 파일 이름 규칙 --> 프로젝트ID_models.txt
    url = 'media/files/' + fileName
    with open(url, 'w', encoding='utf-8') as outFile:
        json.dump(sequence_json, outFile, ensure_ascii=False, indent="\t")

    context = {}

    return HttpResponse(json.dumps(context), content_type="application/json")

############################################################################
############################################################################
############################################################################
# class LoginPageView(TemplateView):
#     template_name = "data.html"
#     def get(self, request, **kwargs):
#         print(request)
#         return render(request, 'login.html')

#     def get_context_data(self, **kwargs):
#         context = super(ModelingView_data, self).get_context_data(**kwargs)
#         name = "helloworld"
#         print(name)
#         context['name'] = name
#         return context

############################################################################
############################################################################
############################################################################
def getTrainingResult(request):
    epoch = request.POST.get('epoch')

    template = loader.get_template('training.html')     # response 템플릿 지정

    # loss = select_loss(epoch)[0][0] 
    # accuracy = select_accuracy(epoch)[0][0]
    training_result = select_training_result(epoch)
    train_accuracy = training_result[0][1]
    train_loss = training_result[0][2] 
    val_accuracy = training_result[0][3]
    val_loss = training_result[0][4]

    ETA = select_ETA(epoch)[0][1]

    resource_result = select_resource(epoch)
    print(resource_result)
    mem_usage = resource_result[0][1]
    cpu_usage = resource_result[0][2]
    net_usage = resource_result[0][3]

    # print(mem_usage)
    # print(cpu_usage)
    # print(net_usage)

    context = {'train_loss': train_loss, 
               'train_accuracy': train_accuracy,
               'val_accuracy': val_accuracy, 
               'val_loss': val_loss,
               'ETA' : ETA,
               'mem_usage' : mem_usage,
               'cpu_usage' : cpu_usage,
               'net_usage' : net_usage, }

    # print(train_accuracy)
    # print(train_loss)
    # print(val_accuracy)
    # print(val_loss)
    # print(ETA)
    train_loss = select_result_accuracy()
    print(train_loss)

    return HttpResponse(json.dumps(context), content_type="application/json")

############################################################################
############################################################################
############################################################################
def select_result(request):

    template = loader.get_template('training.html')     # response 템플릿 지정

    
    train_loss = select_result_accuracy()
    train_accuracy = select_result_accuracy()
    val_loss = select_result_accuracy()
    val_accuracy = select_result_accuracy()

    # print(train_loss)

    print("train_loss",train_loss)

    #test = select_training_result(epoch)
    # context = {'tableName': tableName,
    #            'tuples': csvTable,
    #            'column': column }
    context = {'train_loss': train_loss, 
               
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

#####################################################################
#### CBV File View
#####################################################################
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import render

class FileUploadView(View):
    form_class = DocumentForm               # form 클래스 설정
    success_url = reverse_lazy('model_base')    # 성공시 'upload'라는 alias를 갖는 url로 이동
    template_name = 'model.html' 

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES, auto_id=False)

        if form.is_valid():
            form.save('media/myJSON/')
<<<<<<< HEAD
            documents = Document.objects.last()                     # get the last document which means uploaded one lastly.
            data = createAndInsert_json(documents.document)         # 1. json --> diagram
            # data = code2diagram(documents.document)               # 2. exeScript --> diagram
            file_name = str(documents.document)[0:-5]

            # data = createAndInsert_json(documents.document)     # document를 추가하는 비지니스로직 수행
            
            # Parse JSON file to JSON dump
            # return context(json dump)
            # return redirect(self.success_url)
            # print(json.dumps(data))
            # test = str(data)
            return render(request, self.template_name, {'foo': json.dumps(data), "file_name": file_name})
        else:
            return render(request, self.template_name, {'form': form})

class Testview(View):
    form_class = DocumentForm               # form 클래스 설정
    success_url = reverse_lazy('model_base')    # 성공시 'upload'라는 alias를 갖는 url로 이동
    template_name = 'myTest.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES, auto_id=False)

        if form.is_valid():
            form.save('media/myJSON/')
=======
>>>>>>> 482236f8f85831ba515214b518197ad8b82f3b72
            documents = Document.objects.last()
            data = code2diagram(documents.document)

            # data = createAndInsert_json(documents.document)     # document를 추가하는 비지니스로직 수행
<<<<<<< HEAD

=======
            
>>>>>>> 482236f8f85831ba515214b518197ad8b82f3b72
            # Parse JSON file to JSON dump
            # return context(json dump)
            # return redirect(self.success_url)
            print(json.dumps(data))
            # test = str(data)
            return render(request, self.template_name, {'foo': json.dumps(data)})
        else:
            return render(request, self.template_name, {'form': form})