from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from display_table.views import DisplayTableView

urlpatterns = [
    url('', DisplayTableView.as_view()),

]