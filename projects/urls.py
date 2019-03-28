from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from projects.views import *

urlpatterns = [
    #url('$', ModelingView_model.as_view()),
    ### 현재 자신의 프로젝트 목록을 불러오는 프로젝트 메인 페이지
    #url('projects/', ModelingView_data.as_view()),

    ### 사용자 프로젝트 페이지 :: projects/myPage/
    url('myProject/$', MyProjectView.as_view(), name="myProject"),

    ### 프로젝트 생성 페이지 :: projects/myPage/create_project/
    url('myProject/create_project/$', CreateProjectView.as_view()),

    ### 프로젝트 삭제 페이지 :: projects/myPage/delete_project/
    url('myProject/delete_project/$', DeleteProjectView.as_view()),

    ### 프로젝트 샘플 페이지 :: projects/sample_project/
    url('sample_project/$', ProjectSampleProjectView.as_view()),


]