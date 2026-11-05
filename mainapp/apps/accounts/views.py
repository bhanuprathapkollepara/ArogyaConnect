from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "GET":
        return render(request, "accounts/singup.html")
    return HttpResponse("Signup is not implemented.", status=501)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")
    return HttpResponse("Login is not implemented.", status=501)
