"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import ListView, DetailView
from bookmark.views import BookmarkLV, BookmarkDV
from bookmark.models import Bookmark
from mysite.views import *
from modeling.views import *
from django.conf.urls import url
from projects.views import *
from autoML_agent.views import *

urlpatterns = [
    #### admin page ####
    path('admin/', admin.site.urls),

    #### main home page ####
    path('', home_redirect),
    #path('home/', HomeView.as_view(), name='home'),
    path('home/', MyProjectView.as_view()),

    #### bookmark page ####
    path('bookmark/', include('bookmark.urls')),
    #path('bookmark/', BookmarkLV.as_view(), name='index'),
	path('bookmark/<pk>/', BookmarkDV.as_view(), name='detail'),

	#### data set upload page ####
    path('upload/', include('upload.urls')),

    #### display table page ####
    path('display_table/', include('display_table.urls')),

    #### modeling page ####
    #url(r'^modeling/', include('modeling.urls')),
    path('modeling/', include('modeling.urls')),

    #### environments page ####
    #url(r'^modeling/', include('modeling.urls')),
    path('environments/', include('environments.urls')),

    #### projects page ####
    #url(r'^modeling/', include('modeling.urls')),
    path('projects/', include('projects.urls')),

    ### account page ###
    url('accounts/', include('django.contrib.auth.urls')),
    url('accounts/register/$', UserCreateView.as_view(), name='register'),
    url('accounts/register/done/$', UserCreateDoneTV.as_view(), name='register_done'),

    #### jobplan page ####
    # path('jobPlan/', include('jobPlan.urls')),

    ### automl page ###
    path('autoML_agent/', include('autoML_agent.urls')),

    
]
