from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from verify_email.email_handler import send_verification_email
from accounts.forms import RegistrationForm


class LoginView(View):
    def get(self, request):
        logout(request)
        return render(request, "accounts/login_form.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect("main:home")
                else:
                    messages.error(request, "User registration incomplete!")
                    redirect("request-new-link-from-email")
            except Exception as e:
                messages.error(request, f"{e}")
        messages.error(request, "Invalid user credentials!")
        return render(request, "accounts/login_form.html")


class RegisterView(View):
    def get(self, request):
        logout(request)
        form = RegistrationForm()
        return render(request, "accounts/register_form.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        try:
            if form.is_valid():
                try:
                    form.clean_passwords()
                    form.save()
                    send_verification_email(request, form)
                    messages.success(
                        request,
                        "A verification email has been sent to your email address",
                    )
                    return redirect("accounts:login_page")

                except Exception as e:
                    messages.error(request, str(e).strip("[]''"))
                    return redirect("accounts:review_view")
            else:
                messages.error(request, "Invalid form credentials")
        except Exception as e:
            messages.error(request, str(e))
        return redirect("accounts:register_view")


class LogoutView(LoginRequiredMixin, View):
    login_url = "accounts:login_page"
    redirect_field_name = "login_page"

    def get(self, request):
        logout(request)
        messages.success(request, "Logout Successful")
        return redirect("accounts:login_page")
