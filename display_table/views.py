from django.views.generic import ListView, DetailView
from display_table.models import Table
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from upload.models import Document
from static.script.script import *


class DisplayTableView(ListView):
    model = Table                               # 모델 설정
    context_object_name = 'table'               # 컨텍스트 객체 이름 지정
    template_name = 'tables_dynamic.html'       # 템플릿 파일 지정

    def get_context_data(self, **kwargs):
        context = super(DisplayTableView, self).get_context_data(**kwargs)

        ############### 테이블로부터 object를 가져온다(.csv)
        documents = Document.objects.last()             # 가장 최근 삽입된 파일을 불러온다.
        tableName = getTableName(documents.document)    # 파일경로로부터 테이블 이름을 추출
        csvTable = selectData(tableName)                # 튜플 select
        column = getColumnName(tableName)               # 컬럼명 추출

        context['column'] = column              # 컬럼명 저장
        context['csvTable'] = csvTable          # 튜플목록 저장

        return context
