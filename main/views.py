from django.shortcuts import redirect, render
from django.views.generic import View
from accounts.models import User
from main.models import AccessKey, KeyToken
from main.services import LoginMixin, send_key_token
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
        send_key_token(user=user)
        ctx = {
            "user": user,
        }
        return render(request, "main/request_key.html", ctx)

    def post(self, request, uuid):

        token = request.POST["token"].strip(" ")

        try:
            user = User.objects.get(id=uuid)
            acces_token = KeyToken.objects.get(key=token)
            if acces_token.status == "EXPIRED":
                messages.error(request, "Token has expired!")
                return render(request, "main/request_key.html", {"user": user})

        except Exception as e:
            messages.error(request, f"{e}")
            return render(request, "main/request_key.html", {"user": user})
        if acces_token.user == user and acces_token:
            keys = AccessKey.objects.filter(user=user)
            for key in keys:
                if key.status == "ACTIVE":
                    messages.error(request, "Current key is not expired yet!")
                    return redirect("main:home")

            new_key = AccessKey.objects.create(user=user)
            new_key.clean()
            new_key.save()
            acces_token.status = "EXPIRED"
            acces_token.save()
            return redirect("main:home")
        messages.error(request, "an error occured")
        return render(request, "main/request_key.html", {"user": user})
