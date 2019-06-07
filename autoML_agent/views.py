from autoML_agent.forms import *
from static.script.script import *
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import render
import json
from autoML_agent.models import *
from django.template import RequestContext, loader, Context
from django.http import HttpResponse


class taskGenerationView(View):
    print("!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!")
    form_class = DocumentForm               # form 클래스 설정
    success_url = reverse_lazy('task_generation')    # 성공시 'upload'라는 alias를 갖는 url로 이동
    template_name = 'task_generation.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES, auto_id=False)

        if form.is_valid():
            form.save('media/myJSON/')
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

class taskFlowView(View):
    print("!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!!@#!#!@#@!#@!#@!")
    form_class = DocumentForm               # form 클래스 설정
    success_url = reverse_lazy('task_flow')    # 성공시 'upload'라는 alias를 갖는 url로 이동
    template_name = 'task_flow.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES, auto_id=False)

        if form.is_valid():
            form.save('media/myJSON/')
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

##### Ajax --- Table
def getTable(request):
    tableName = request.POST.get('dataSet')
    print(tableName)

    template = loader.get_template('task_flow.html')     # response 템플릿 지정

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