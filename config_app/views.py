from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MasterConfig
from .serializers import (
    MasterConfigSerializer,ConfigSerializer
)
from rest_framework import generics, mixins
from auth_app.common.errors import ClientErrors, DatabaseErrors, UserErrors
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# from auth_app.common.functions import get_date_datetime, get_string_datetime


class CreateCategoryOrSubcategoryView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    serializer_class = MasterConfigSerializer
    permission_classes = [IsAuthenticated]
    queryset = MasterConfig.objects.all()

 
    def post(self, request):
        try:

            data = request.data
            serializer = MasterConfigSerializer(data=data)
            if not serializer.is_valid(raise_exception=False):
                err = " ".join(
                    [
                        f"{field}: {', '.join(error)}"
                        for field, error in serializer.errors.items()
                    ]
                )
                raise ClientErrors(err)

            serializer.save()
            return Response(
                {"message": "Category is Successfully Created", "success": True},
                status=status.HTTP_201_CREATED,
            )
        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                },
                status=error.response_code,
            )
        
    def put(self, request, pk=None, *args, **kwargs):
        id = pk
        if id is not None:
            try:
                emp = MasterConfig.objects.get(id=id)
            except MasterConfig.DoesNotExist:
                return Response(
                    {
                        "message": "Given Category not found",
                        "success": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = MasterConfigSerializer(emp, data=request.data)
            if not serializer.is_valid(raise_exception=False):
                err = ""
                for field, error in serializer.errors.items():
                    err += "{}: {} ".format(field, ",".join(error))
                raise ClientErrors(err)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Given Category has been updated",
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "Invalid data provided",
                        "errors": serializer.errors,
                        "success": False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "message": "Category id is not valid",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
  
    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params.get("id")
            if not id:
                total_qs = MasterConfig.objects.filter(parent__isnull=True)
                serializer = ConfigSerializer(total_qs, many=True)
                return Response(
            {
                "data": serializer.data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
            master_configs = MasterConfig.objects.filter(id=id, )  # Fetch top-level configurations
            serializer = MasterConfigSerializer(master_configs, many=True)
            return Response(
            {
                "data": serializer.data,
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
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        

    def delete(self, request, pk=None):
        try:
            self.destroy(request, pk)
            return Response(
                        {
                            "message": "Given Category is Deleted",
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

 
