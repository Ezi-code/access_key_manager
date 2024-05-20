from django.shortcuts import redirect, render
from django.views.generic import View
from accounts.models import User
from main.models import AccessKey, KeyToken
from main.services import SendMail, LoginMixin
from django.contrib import messages


class HomeView(LoginMixin, View):
    def get(self, request):
        active_keys = AccessKey.objects.filter(user=request.user, status="ACTIVE")
        revoked_keys = AccessKey.objects.filter(user=request.user, status="REVOKED")
        expired_keys = AccessKey.objects.filter(user=request.user, status="EXPIRED")
        ctx = {
            "active_keys": active_keys,
            "revoked_keys": revoked_keys,
            "expired_keys": expired_keys,
        }
        return render(request, "main/home.html", ctx)

    def post(self, request):
        key = AccessKey.objects.get(user=request.user)
        return render(request, "main/home.html", {"key": key})


class RequestKeyView(LoginMixin, View):
    def get(self, request, uuid):
        user = User.objects.get(id=uuid)
        SendMail.send_key_token(user)
        ctx = {
            "user": user,
        }
        return render(request, "main/request_key.html", ctx)

    def post(self, request, uuid):
        user = User.objects.get(id=uuid)
        token = request.POST["token"]
        acces_token = KeyToken.objects.get(key=token)
        if acces_token.user == user:
            keys = AccessKey.objects.filter(user=user)
            for key in keys:
                if key.status == "ACTIVE":
                    messages.error(request, "Current key is not expired yet!")
                    return redirect("main:home")
                else:
                    new_key = AccessKey.objects.create(user=user)
                    new_key.clean()
                    new_key.save()
                    return redirect("main:home")
        return render(request, "main/request_key.html", {"user": user})