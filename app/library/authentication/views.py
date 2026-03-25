from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from .decorators import role_required
from .models import CustomUser
from order.models import Order

from django.http import HttpResponseRedirect
from authentication.forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = CustomUser.objects.create_user(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                middle_name=data['middle_name'],
                role=int(data['role']),
                is_active=True
            )

            if user:
                return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            email = data["email"]
            password = data["password"]

            user_exists = CustomUser.get_by_email(email)

            if user_exists:
                user = authenticate(request, username=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('home')

        return render(request, "login.html", {
            "form": form,
            "error": "Invalid email or password"
        })

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@role_required(1)
def user_admin_list(request):
    users = CustomUser.get_all().order_by("id")
    return render(request, "user_admin_list.html", {"users": users})


@role_required(1)
def user_admin_detail(request, pk):
    user_obj = CustomUser.get_by_id(pk)
    if user_obj is None:
        raise Http404
    return render(request, "user_admin_detail.html", {"user_obj": user_obj})

@role_required(1)
def user_books(request, pk):
    user_obj = CustomUser.get_by_id(pk)

    if user_obj is None:
        raise Http404

    orders = Order.objects.filter(user=user_obj, end_at__isnull=True)

    return render(request, "user_books.html", {
        "user_obj": user_obj,
        "orders": orders,
    })
