from django.conf.urls import url
#from upload.views import Upload
from django.conf.urls.static import static
from django.conf import settings
from upload.views import *

urlpatterns = [
    # url('', model_form_upload),

    # url('upload_file/', model_form_upload),
    url('', FileUploadView.as_view(), name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)