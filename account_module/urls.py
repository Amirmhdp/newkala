from django.urls import path

from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.Logout.as_view(), name='logout_page'),
    path('forgot-password', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('reset-password/<change_password_code>', views.ResetPasswordView.as_view(), name='reset_password_page'),
    path('active-account/<email_active_code>', views.ActivateAccount.as_view(), name='email_active_code')
]