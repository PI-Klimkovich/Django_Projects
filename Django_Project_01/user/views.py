from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest

from .models import User


def register(request: WSGIRequest):
    if request.method != "POST":
        return render(request, "registration/register.html")
    if not request.POST.get("username") or not request.POST.get("email") or not request.POST.get("password1"):
        return render(
            request,
            "registration/register.html",
            {"errors": "Укажите все поля!"}
        )

    # Если уже есть такой пользователь с username или email.
    # if User.objects.filter(
    #         Q(username=request.POST["username"]) | Q(email=request.POST["email"])
    # ).count() > 0:
    #     return render(
    #         request,
    #         "registration/register.html",
    #         {"errors": "Пользователь с username или email уже зарегистрирован"}
    #     )

    # Если есть пользователь с таким username.
    if User.objects.filter(Q(username=request.POST["username"])).count() > 0:
        return render(
            request,
            "registration/register.html",
            {"errors": f"Пользователь с username '{request.POST.get('username')}' уже зарегистрирован"}
        )


    # Сравниваем два пароля!
    if request.POST.get("password1") != request.POST.get("password2"):
        return render(
            request,
            "registration/register.html",
            {"errors": "Пароли не совпадают"}
        )

    # Создадим учетную запись пользователя.
    # Пароль надо хранить в БД в шифрованном виде.
    User.objects.create_user(
        username=request.POST["username"],
        email=request.POST["email"],
        password=request.POST["password1"]
    )
    return HttpResponseRedirect(reverse('reg_ok'))


def about_registration(request):
    return render(request, "user/reg_ok.html")
