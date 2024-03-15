from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
# Create your views here.


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('voice:home')
            
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('voice:voice')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username yoki parol noto\'g\'ri'})
        

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('voice:voice')
    def post(self, request):
        return redirect('voice:voice')
    

