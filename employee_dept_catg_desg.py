import datetime
import json
import os
import json
import requests

import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'committee_module_ops.settings')
application = get_wsgi_application()
django.setup()

from django.conf import settings

from config_app.models import MasterConfig
from committee_app.models import EmployeeInfo
api_url = "https://tech.kiet.edu/api/hrms/commitee_migrate/?token=$3RP@(4"
response = requests.get(api_url)
response.raise_for_status()  # Raise an error for bad responses
data = response.json()

for item in data:
            if item.get('dept__value') is not None and item.get('emp_category__value') is not None and item.get('desg__value') is not None:
            
            # Create or get department, category, designation objects from MasterConfig
                department_parent = MasterConfig.objects.get(label = "DEPARTMENT")
                category_parent = MasterConfig.objects.get(label = "CATEGORY OF EMPLOYEE")
                designation_parent = MasterConfig.objects.get(label = "DESIGNATION")
                department, created = MasterConfig.objects.get_or_create(label=item['dept__value'], parent =department_parent)
                category, created = MasterConfig.objects.get_or_create(label=item['emp_category__value'], parent =category_parent)
                designation, created = MasterConfig.objects.get_or_create(label=item['desg__value'], parent =designation_parent)

                # Create EmployeeInfo object
                employee = EmployeeInfo.objects.create(
                    employee_name=item['name'],
                    department=department,
                    category_of_employee=category,
                    designation=designation,
                    # Add other fields as needed
                )

                # Save the EmployeeInfo object
                employee.save()
