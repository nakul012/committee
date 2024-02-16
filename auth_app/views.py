import base64
import csv
import os
from rest_framework.parsers import FileUploadParser
from django.http import HttpRequest, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
import requests
# from auth_app.common.functions import check_password, generate_password
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_app.models import Account
from auth_app.common.errors import ClientErrors, DatabaseErrors, UserErrors
from auth_app.common.tokens import get_access_token, encode_token
from django.conf import settings

from auth_app.common.emailer import email_verify
from auth_app.common.functions import generate_password
from .serializers import (
    SignUpSerializer,
    UserLoginSerializer,
   
)
from django.http import FileResponse
from oauth2_provider.models import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


BASE_URL = settings.BASE_URL


class UserSignUpView(APIView):
    def post(self, request: HttpRequest) -> Response:
        """
        User SignUp API

        POST:
        Create a new User and return auth token
        """
        try:
            serializer = SignUpSerializer(data=request.data)
            if not serializer.is_valid(raise_exception=False):
                err = ""
                for field, error in serializer.errors.items():
                    err += "{}: {} ".format(field, ",".join(error))
                raise ClientErrors(err)
            if Account.objects.filter(email=request.data["email"]):
                raise ClientErrors(message="Account already exists", response_code=400)
            # password_check = check_password(request.data["password"])
            # if password_check:
            serializer.save()
            user = Account.objects.last()
            
            
            email = request.data["email"]
            password = generate_password()
            user.set_password(password)
            user.save()
            user_token = get_access_token(user=user)
            token = user_token["access_token"]
            enc_token = encode_token(token)
            link = "Passowrd=" + password
            try:
                # modifying temporarily. you can check the original version from erp code
                email_verify(f"Account Password  ", email, link)

                # email_verify("Account Verification Email - ERP 3.0\n {password}", email, link)
            except:
                UserErrors(message="Please check your Email ID.", response_code=500)
            return Response(
                {
                    "message": "Account Created Successfully,and a verification link has been sent on email.",
                    "success": True,
                    "token": enc_token,
                },
                status=status.HTTP_200_OK,
            )
            # else:
            #     raise Exception(password_check)
        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                },
                status=error.response_code,
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserLoginView(APIView):
    def post(self, request):
        """
        Operation Team Login API

        POST:
        Login Ops user and return new auth token
        """
        try:
            serializer = UserLoginSerializer(data=request.data)
            if not serializer.is_valid(raise_exception=False):
                err = " ".join(
                    [
                        f"{field}: {', '.join(error)}"
                        for field, error in serializer.errors.items()
                    ]
                )
                raise ClientErrors(err)
            user = serializer.validated_data["user"]
            token = get_access_token(user)
            return Response(
                {
                    "message": "Logged In Successfully",
                    "token": token,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )

        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                },
                status=error.response_code,
            )
        # except Exception as error:
        #     return Response(
        #         {
        #             "message": "Something Went Wrong",
        #             "success": False,
        #         },
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )


class UserLogoutView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request: HttpRequest) -> Response:
        """
        Logout API For Ops User

        param:
            usertoken in AUTH PARAMETER
        """
        try:
            user_token = request.auth
            refresh_tokens = RefreshToken.objects.filter(access_token=user_token)
            refresh_tokens.delete()
            user_token.delete()
            return Response(
                {
                    "message": "You are successfully logout",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )