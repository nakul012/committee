from django.contrib import admin
from .models import (
    EmployeeInfo, CommitteeInfo, RoleCommitteeInfo
)

admin.site.register(EmployeeInfo)
admin.site.register(CommitteeInfo)
admin.site.register(RoleCommitteeInfo)