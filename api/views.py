from api.serializers import AccessKeySerializer
from rest_framework.views import APIView
from main.models import AccessKey
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class AccountsDetails(APIView, IsAuthenticated):
    serializer_class = AccessKeySerializer

    def get(self, request):
        email = request.query_params.get("email", None)

        if email:
            user = User.objects.filter(email=email).first()
            if user:
                active_key = AccessKey.objects.filter(
                    user=user, status=AccessKey.KeyStatus.ACTIVE
                ).first()
                if active_key:
                    serializer = AccessKeySerializer(active_key)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"detail": "No active key found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                return Response(
                    {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {"detail": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST
        )
