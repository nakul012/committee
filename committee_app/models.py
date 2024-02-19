from django.db import models
from auth_app.models import AbstractTime



class EmployeeInfo(AbstractTime):
    employee_name = models.CharField(
        "Name", max_length=100
    )
    emp_code = models.CharField(
        "Employee ID", max_length=100, unique=True
    )

    department = models.CharField(
        "Department", max_length=100
    )
    organization = models.CharField(
        "Organization", max_length=100, null=True, blank=True
    )
   
   
    type_of_employment = models.CharField(
        "Type of Employment", max_length=100, null=True, blank=True
    )
    category_of_employee = models.CharField(
        "Category Of Employee", max_length=100
    )
    designation = models.CharField(
        "Designation", max_length=100
    )


    def __str__(self):
        return self.employee_name
    

class CommitteeInfo(AbstractTime):    
    committee_name = models.CharField(
        "Name", max_length=100
    )
    description = models.CharField(
        "Descrption", max_length=500, null=True, blank=True, unique=True
    )
    level_type = models.CharField(
        "Level Type", max_length=500, null=True, blank=True, unique=True
    )

    def __str__(self):
        return self.committee_name

class RoleCommitteeInfo(AbstractTime):
    employee = models.ManyToManyField(
        EmployeeInfo, related_name="rolecommitteeinfo_employeeinfo", blank=True, null=True
    )
    committee = models.ForeignKey(
        CommitteeInfo,
        on_delete=models.CASCADE,
        related_name="rolecommitteeinfo_committeeinfo",
        blank=True, null=True
    )
    committee_role_name = models.CharField(
        "Name", max_length=100
    )
    role_per_employee = models.IntegerField(blank=True, null=True)

    description = models.CharField(
        "Descrption", max_length=500, null=True, blank=True
    )

    def __str__(self):
        return self.role_name

