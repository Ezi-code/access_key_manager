from django.shortcuts import render, redirect
from django.views.generic import View
from accounts.models import EmailToken, User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from accounts.services import send_confirmation_code
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login_form.html")
    
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                if user.is_registration_complete:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect("main:home")
                else:
                    messages.error(request, "User registration incomplete!")
                    redirect("accounts:confirm_email", user.id)
            except Exception as e:
                messages.error(request, f"{e}")
        messages.error(request, "Invalid user credentials!")
        return render(request, "accounts/login_form.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register_form.html")

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password1 = request.POST["password1"]
        if password == password1:
            new_user = User.objects.create_user(
                email=email, username=username, password=password
            )
            new_user.full_clean()
            new_user.save()
            send_confirmation_code(new_user)
            return redirect("accounts:confirm_email", new_user.id)
        else:
            messages.error(request, "Passwords do not match!")
        return render(request, "accounts/register_form.html")


class ConfirmEmailView(View):

    def get(self, request, uuid):
        email = User.objects.get(id=uuid).email
        user_id = User.objects.get(id=uuid).id
        ctx = {"email": email, "user_id": user_id}
        return render(request, "accounts/confirm_email.html", ctx)

    def post(self, request, uuid):
        user = User.objects.get(id=uuid)
        code = int(request.POST["code"])
        verification_code = EmailToken.objects.get(user=user).code
        if code == verification_code:
            user.is_registration_complete = True
            user.clean()
            user.save()
            messages.success(request, "Email Verified Successfully")
            return redirect("accounts:login_view")

        messages.error(request, "Invalid Verification Code")
        return render(request, "accounts/confirm_email.html", {"user_id": user.id})


class LogoutView(View, LoginRequiredMixin):
    redirect_field_name = "accounts:login_view"

    def get(self, request):
        logout(request)
        messages.success(request, "Logout Successful")
        return redirect("accounts:login_view")
