from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from projects.models import Projects
from django.http import HttpResponse
from mysite.views import LoginRequiredMixin
import json
from django.urls import reverse_lazy

# 사용자 프로젝트 뷰
class MyProjectView(LoginRequiredMixin, ListView):
    model = Projects     
    context_object_name = 'project_list'                          # 모델 설정
    template_name = "myProject.html"

    def get_queryset(self):
        return Projects.objects.filter(owner=self.request.user)

# # 프로젝트 생성 뷰
# class ProjectCreateView(LoginRequiredMixin, ListView):
#     model = Projects                               # 모델 설정
#     template_name = "create_projects.html"


class ProjectSampleProjectView(LoginRequiredMixin, ListView):
    model = Projects                               # 모델 설정
    template_name = "plain_page.html"


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Projects
    # fields = '__all__'
    fields = ['projectName', 'projectDescription', 'projectTag']
    success_url = "/projects/myProject/"
    
    def form_valid(self, form):
        if self.request.is_ajax:
            form.instance.projectName = self.request.POST.get('project_name')
            form.instance.projectDescription = self.request.POST.get('project_description')
            form.instance.projectTag = self.request.POST.get('project_tags')
            form.instance.owner = self.request.user
            self.object = form.save()
            return HttpResponse(json.dumps("success"), content_type="application/json")
        return super(CreateProjectView, self).form_valid(form)



class DeleteProjectView(LoginRequiredMixin, DeleteView):
    def delete(self, request, *args, **kwargs):
        table_filter = request.POST.get('project_name')
        Project = Projects.objects.filter(projectName=table_filter)
        Project.delete()
        # payload = {'delete  ': 'ok'}
        return HttpResponse(json.dumps("success"), content_type='application/json')



def createNewProject(request):
    model = Projects
    project_name = request.POST.get('project_name')
    project_description = request.POST.get('project_description')
    project_tags = request.POST.get('project_tags')
    print("project_name=", project_name)
    print("project_description=", project_description)
    print("project_tags=", project_tags)

    def form_valid(self, form):
        form.instance.owner = self.request.user
    
    ##### select project
    # selectProject(userId, project_name )
    ##### insert into table :: projects
    # insertProject(userId, project_name, project_description, prject_tags)
    # sequence_json = ast.literal_eval(sequence)      # string 형태를 dictionary객체로 변환
    # print(test.get('op_0'))
    # print(test.get('op_0').get('operator_title'))
    # print(test.get('op_0').keys())


    # ############### .txt 형식으로 json 객체(딕셔너리)를 저장한다 --> /static/files/ + 프로젝트id_models.txt
    # projectId = "2"         # 프로젝트 ID --> 자동생성 해야 함
    # fileName = projectId + "_models.txt"    # 저장할 파일 이름 규칙 --> 프로젝트ID_models.txt
    # url = 'media/files/' + fileName
    # with open(url, 'w', encoding='utf-8') as outFile:
    #     json.dump(sequence_json, outFile, ensure_ascii=False, indent="\t")

    context = { }

    return HttpResponse(json.dumps(context), content_type="application/json")