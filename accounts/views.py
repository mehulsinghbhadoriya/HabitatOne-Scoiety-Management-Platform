from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_default_redirect_url(self):
        if self.request.user.role == 'ADMIN':
            return reverse_lazy('dashboard:admin_home')
        return reverse_lazy('dashboard:resident_home')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('accounts:login')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('dashboard:home')
    
    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully updated.")
        return super().form_valid(form)
