from django.views.generic.base import TemplateView

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.S

# /projects/myProject/ 로 리다이렉트 한다.
def home_redirect(request):
    # object = MyModel.objects.get(...)
    return redirect('/projects/myProject/') #or return redirect('/some/url/')

#--- TemplateView
class HomeView(TemplateView):
    template_name = 'index.html'

#--- User Creation
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

#--- @login_required
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

