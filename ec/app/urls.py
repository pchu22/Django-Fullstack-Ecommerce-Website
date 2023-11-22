from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from . import views
from .forms import LoginForm, ResetPasswordEmailForm

urlpatterns = [
    path('', views.home),

    #login authentication
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='Login'),
    path('signup/', views.CostumerRegistration.as_view(), name='Signup'),
    path('reset-password/', auth_view.PasswordResetView.as_view(template_name='app/reset-password.html', form_class=ResetPasswordEmailForm), name='ResetPasswordEmail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)