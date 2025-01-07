from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz! Iltimos tizimga qayta kiring!")
            return redirect('user:login')  # Login sahifangiz URL'iga yo'naltirish
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Foydalanuvchini tekshirish
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Tizimga kiritish
            login(request, user)
            return redirect('home:home')  # Home sahifaga yo'naltirish
        else:
            # Xato xabar chiqarish
            return render(request, 'login.html', {'error': 'Login yoki parol noto\'g\'ri'})
    return render(request, 'login.html')

def logout_view(request):
    # Foydalanuvchini tizimdan chiqarish
    logout(request)
    return redirect('user:login')  # Login sahifaga yo'naltirish