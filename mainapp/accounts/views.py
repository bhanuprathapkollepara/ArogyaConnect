from django.shortcuts import redirect, render


def signup(request):
    role = request.GET.get("role", request.POST.get("role", "patient"))

    if request.method == "POST":
        role = request.POST.get("role", role)
        return redirect(f"/accounts/login/?role={role}")

    return render(request, "accounts/signup.html", {"role": role})


def login_view(request):
    role = request.GET.get("role", "patient")
    if request.method == "POST":
        return redirect("/accounts/dashboard/")
    return render(request, "accounts/login.html", {"role": role})


def dashboard(request):
    return render(request, "accounts/dashboard.html")

