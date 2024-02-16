
from django.db import models
from auth_app.models import AbstractTime



class EmployeeInfo(AbstractTime):
    name = models.CharField(
        "Name", max_length=100
    )
    emp_code = models.CharField(
        "Employee ID", max_length=100, unique=True
    )
    # department = models.ManyToManyField(
    #     MasterConfig, related_name="basicempinfo_department"
    # )
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
        return self.user_id.email
    

class CommitteeInfo(AbstractTime):    
    emp_id = models.OneToOneField(
        EmployeeInfo,
        on_delete=models.CASCADE,
        related_name="basicempinfo_primempinfo",
    )
    description = models.CharField(
        "Descrption", max_length=500, null=True, blank=True, unique=True
    )

    def __str__(self):
        return self.emp_id.user_id.email

class RoleCommitteeInfo(AbstractTime):
    employee = models.ManyToManyField(
        EmployeeInfo, related_name="basicempinfo_department"
    )
    committee = models.ForeignKey(
        CommitteeInfo,
        on_delete=models.CASCADE,
        related_name="committeeinfo_uploadfile_medical_certificate",
        blank=True, null=True
    )
    name = models.CharField(
        "Name", max_length=100
    )
    role_per_employee = models.IntegerField(blank=True, null=True)
    description = models.CharField(
        "Descrption", max_length=500, null=True, blank=True, unique=True
    )

    def __str__(self):
        return self.emp_id.user_id.email

