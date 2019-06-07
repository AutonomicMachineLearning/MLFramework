from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from autoML_agent.views import *
from django.urls import path


urlpatterns = [
    #url('$', ModelingView_model.as_view()),
    url('task_generation/$', taskGenerationView.as_view(), name='task_generation'),
    url('task_flow/$', taskFlowView.as_view(), name='task_flow'),
    url('task_flow/table/', getTable),

    # url('', FileUploadView.as_view(), name='upload'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)