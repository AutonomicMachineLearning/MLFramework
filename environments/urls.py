from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from environments.views import *

urlpatterns = [
    #url('$', ModelingView_model.as_view()),
    url('', Environments_view.as_view()),

]