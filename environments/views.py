from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from environments.models import Environments

class Environments_view(ListView):
    model = Environments                               # 모델 설정
    template_name = "environments.html"