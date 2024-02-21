from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CommitteeInfo, EmployeeInfo, RoleCommitteeInfo
from config_app.models import MasterConfig
# from .models import MasterConfig
from .serializers import (
    AssignCommitteeSerializer, CommitteeInfoSerializer, 
)
from rest_framework import generics, mixins
from auth_app.common.errors import ClientErrors, DatabaseErrors, UserErrors
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# from auth_app.common.functions import get_date_datetime, get_string_datetime


class AssignCommitteeView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    serializer_class = AssignCommitteeSerializer
    permission_classes = [IsAuthenticated]


 
    def post(self, request):
        try:

            data = request.data
            committee_info_created = False
            serializer = AssignCommitteeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            if not serializer.is_valid(raise_exception=False):
                err = " ".join(
                    [
                        f"{field}: {', '.join(error)}"
                        for field, error in serializer.errors.items()
                    ]
                )
                raise ClientErrors(err)
            validated_data = serializer.validated_data
            level_type = int(validated_data["level_type"])
            type_of_committee = int(validated_data["type_of_committee"])
            description = validated_data["description"]
            roles = validated_data["roles"]
            seen3 = []

            # create department wise employee
            for role in roles:
                seen = {}     
                seen2 = {}
                seen["role"] = int(role["role"])
                seen["count"] = int(role["count"])
                seen["department"] = []
                for department_id in role["department"]:
                    seen2["department"] = department_id
                    seen2["employees"] = EmployeeInfo.objects.filter(category_of_employee__id__in=role["category_of_employee"],
        designation__id__in=role["designation"], department_id = department_id)
                    seen["department"].append(seen2)
                    seen2 = {}
                seen3.append(seen)
            total_selected_employee = []
            employee_object_data = []

            # select role wise employees
            for item in seen3:
                selected_employee = {}
                updated_lst_of_employee = []
                lst_of_employee = []
                
                selected_employee["role"] = item["role"]
                selected_employee["count"] = item["count"]
                item['department'] = sorted(item['department'], key=lambda x: len(x['employees']), reverse=True)
                # for i in range(item["count"]):
                count = item["count"]
                
                while count >0:
                    # select employee for all department according to one role.
                    for department in item["department"]:
                        if count == 0:
                            break
                        
                        employee_qs = department["employees"]
                        random_object = employee_qs.order_by('?').first()
                        if random_object:
                            # check the limit for maximum committee assign to employee or employee selected twice to single committee
                            if random_object.committee_count_current >= int(random_object.committee_count_limit.label) or random_object in employee_object_data:
                                employee_qs = employee_qs.exclude(pk=random_object.pk)
                                for obj in employee_qs:
                                    random_object = employee_qs.order_by('?').first()
                                    if random_object.committee_count_current >= int(random_object.committee_count_limit.label) or random_object in employee_object_data:
                                        employee_qs = employee_qs.exclude(pk=random_object.pk)
                                    else:
                                        break
                            else:

                                lst_of_employee.append(random_object)
                                employee_object_data.append(random_object)
                                employee_qs = employee_qs.exclude(pk=random_object.pk)
                                department["employees"] = employee_qs
                                count-=1
                    if len(updated_lst_of_employee)<len(lst_of_employee):
                        updated_lst_of_employee = lst_of_employee
                    else:
                        break
                selected_employee["employees"] = lst_of_employee
                if count>0:
                    label = MasterConfig.objects.get(id=item['role']).label
                    raise ClientErrors(f"Employees are not enought to be selected for this role {label} ")
                total_selected_employee.append(selected_employee)
            if not committee_info_created:
                label = MasterConfig.objects.get(id=type_of_committee)
                level_type = MasterConfig.objects.get(id=int(validated_data["level_type"])) 
                committee_exist = CommitteeInfo.objects.filter(committee=label, level_type=level_type).first()
                if committee_exist:
                    raise ClientErrors("This committee is already exist.")
                committee_info_obj = CommitteeInfo.objects.create(committee=label, level_type=level_type, description=description)
                committee_info_created=True
            
            for data in total_selected_employee:
                role = MasterConfig.objects.get(id=data["role"])
                employee_lst = data["employees"]
                
                role_committee_info_obj= RoleCommitteeInfo.objects.create( committee=committee_info_obj, committee_role=role, role_per_employee=data["count"])
                role_committee_info_obj.employee.set(employee_lst)
                for emp_id in employee_lst:
                    obj = EmployeeInfo.objects.get(id=emp_id.id)
                    obj.committee_count_current +=1
                    obj.save()
                        

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
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
   
        
    def get(self, request, *args, **kwargs):
        try:
            queryset = CommitteeInfo.objects.all()
            serializer = CommitteeInfoSerializer(queryset, many=True)
            
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

