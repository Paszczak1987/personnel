from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.html import format_html
from django.views import View
from staff_hub.forms import RegisterUserForm


# Create your views here.

class BaseView(View):
    def get(self, request):
        return render(request, template_name='base.html')

class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'staff_hub/register_user.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('register_success')
        return render(request, 'staff_hub/register_user.html', {'form': form})
        
class RegisterSuccessView(View):
    def get(self, request):
        return render(request, 'staff_hub/register_success.html')
    
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        self.add_bootstrap_classes(form)
        return render(request, 'staff_hub/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        self.add_bootstrap_classes(form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('home')
        messages.error(request, "Invalid username or password.")
        return render(request, 'staff_hub/login.html', {'form': form})
    
    def add_bootstrap_classes(self, form):
        for field_name, field in form.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': format_html('Enter your {}', field.label.lower())
            })

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    