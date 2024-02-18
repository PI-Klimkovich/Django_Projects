from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q, Count, Value, Subquery, OuterRef
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required

from .models import User
from notes.models import Tag, GroupConcat
# from .models import Note


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
        password=request.POST["password1"],
        country=request.POST["country"],
    )
    return HttpResponseRedirect(reverse('reg_ok'))


def about_registration(request):
    return render(request, "user/reg_ok.html")


def show_user_view(request):
    all_users = (User.objects
                 .annotate(notes_num=Count('note__user'))
                 .values("username", "last_login", "country", "notes_num")
                 .order_by('username'))

    # all_users = (User.objects
    #              .annotate(notes_num=Count('note__user'),
    #                        tag_names=Subquery(
    #                            Tag.objects.filter(notes=OuterRef('pk')).values('notes')
    #                            .annotate(names=GroupConcat('name', Value(' '), distinct=True))
    #                            .values('names')[:1]
    #                        )
    #                        )
    #              .values("username", "last_login", "country", "notes_num")
    #              .order_by('username'))
    print(all_users)
    context: dict = {
        "users": all_users,
    }
    return render(request, "user/users.html", context)


# При условии что (ссылка без username):
# - в urls.py без /<username> --- строка 8
# - в menu.html без user --- строка 31
# - в profile.html без user.username --- строка 22
@login_required
def profile_update_view(request: WSGIRequest):
    user = get_object_or_404(User, username=request.user)
    print(user, user.username, request.user)
    if user != request.user:
        return HttpResponseForbidden("У Вас нет разрешения на редактирование объекта")

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.phone = request.POST.get("phone", user.phone)
        user.save()
        return HttpResponseRedirect("profile_ok")
    tags_queryset = Tag.objects.filter(notes__user=user).distinct()

    return render(request, 'user/profile.html', {'tags': tags_queryset})


# При условии что необходима ссылка с /<username> ---- смотри комментарии выше!!
# @login_required
# def profile_update_view(request: WSGIRequest, username):
#     user = get_object_or_404(User, username=username)
#     print(user, username, user.username, request.user)
#     if user != request.user:
#         return HttpResponseForbidden("У Вас нет разрешения на редактирование объекта")
#
#     if request.method == "POST":
#         user = User.objects.get(username=username)
#         user.first_name = request.POST.get("first_name", user.first_name)
#         user.last_name = request.POST.get("last_name", user.last_name)
#         user.phone = request.POST.get("phone", user.phone)
#         user.save()
#         return HttpResponseRedirect("/")
#     tags_queryset = Tag.objects.filter(notes__user=user).distinct()
#
#     return render(request, 'user/profile.html', {'tags': tags_queryset})


def about_profile(request):
    return render(request, "user/profile_ok.html")
