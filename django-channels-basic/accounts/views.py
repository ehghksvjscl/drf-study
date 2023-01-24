from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

login = LoginView.as_view(
    template_name='partials/form.html',
    extra_context = {
        "form_name": "로그인",
        "submit_name": "로그인",
    }
)

logout = LogoutView.as_view(
    next_page = 'accounts:login'
)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

profile = ProfileView.as_view()

signup = CreateView.as_view(
    form_class = UserCreationForm,
    template_name='partials/form.html',
    extra_context = {
        "form_name": "회원가입",
        "submit_name": "회원가입",
    },
    success_url = reverse_lazy('accounts:login'),
)