from django.db import models
from auth_app.models import AbstractTime
from config_app.models import MasterConfig



class EmployeeInfo(AbstractTime):
    employee_name = models.CharField(
        "Name", max_length=100
    )
    emp_code = models.CharField(
        "Employee ID", max_length=100, unique=True
    )

    department = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="employeeinfo_masterconfig_department",
    )
    organization = models.CharField(
        "Organization", max_length=100, null=True, blank=True
    )
   
   
    type_of_employment = models.CharField(
        "Type of Employment", max_length=100, null=True, blank=True
    )
    category_of_employee = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="employeeinfo_masterconfig_category_of_employee",
    )
    designation = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="employeeinfo_masterconfig_designation",
    )
    committee_count_limit = models.ForeignKey(
        MasterConfig,
        on_delete=models.PROTECT,
        related_name="employeeinfo_masterconfig_committee_count",
    )
    committee_count_current = models.IntegerField(default=0)

    def __str__(self):
        return self.employee_name
    

class CommitteeInfo(AbstractTime):    
    committee = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="committeeinfo_masterconfig_committee",
    )
    description = models.CharField(
        "Descrption", max_length=500, null=True, blank=True
    )
    level_type = models.ForeignKey(
        MasterConfig,
        on_delete=models.PROTECT,
        related_name="committeeinfo_masterconfig_level_type",
    )

    def __str__(self):
        return self.committee.label

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
    committee_role = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="rolecommitteeinfo_masterconfig",
    )
    role_per_employee = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.committee_role.label

