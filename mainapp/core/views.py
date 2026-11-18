from django.shortcuts import redirect, render


def home(request):
    if request.method == "POST":
        role = request.POST.get("role", "patient")
        return redirect(f"/accounts/signup/?role={role}")
    return render(request, "home/home.html")


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")
