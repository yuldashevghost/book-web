from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from apps.users.forms import UserRegistrationForm, LoginForm
from apps.users.models import User


# Authorization
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, "User Successfully created")
            return redirect('users:login')
        return render(request, 'auth/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Logged in successfully as {user.username}')
                return redirect('homepage')

        messages.warning(request, 'Username or password wrong')
        return render(request, 'auth/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Logged out successfully')
        return redirect('homepage')




class ProfileView(DetailView):
    slug_field = "username"
    slug_url_kwarg = "username"
    model = User
    context_object_name = "user"
    template_name = "users/profile.html"
