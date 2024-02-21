from rest_framework import serializers
from .models import *


class RoleSerializer(serializers.Serializer):
    role = serializers.CharField()
    count = serializers.CharField()
    department = serializers.ListField(child=serializers.IntegerField())
    category_of_employee = serializers.ListField(child=serializers.IntegerField())
    designation = serializers.ListField(child=serializers.IntegerField())

class AssignCommitteeSerializer(serializers.Serializer):
    level_type = serializers.CharField()
    description = serializers.CharField( allow_null=True, allow_blank=True)
    type_of_committee = serializers.CharField()
    roles = RoleSerializer(many=True)


class EmployeeInfoSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = EmployeeInfo
        fields = ['id', 'employee_name', 'emp_code', 'department']

    
class CommitteeInfoSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField(read_only=True)
    level_type_name = serializers.CharField(source="level_type.label", read_only=True)
    committee_name = serializers.CharField(source="committee.label", read_only=True)

    class Meta:
        model = CommitteeInfo
        fields = ['id', "level_type_name", 'level_type', "committee_name",'committee', 'description', "roles",]

    def get_roles(self,instance):
        role =  instance.rolecommitteeinfo_committeeinfo.all()
        children_serializer = RoleCommitteeInfoSerializer(role, many=True)
        return children_serializer.data
    



class RoleCommitteeInfoSerializer(serializers.ModelSerializer):
    employee = EmployeeInfoSerializer(many=True, read_only=True)
    role_name = serializers.CharField(source="committee_role.label", read_only=True)


    class Meta:
        model = RoleCommitteeInfo
        fields = ['id','role_name', 'committee_role', 'employee', 'committee']