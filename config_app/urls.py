from django.urls import path
from .views import CreateCategoryOrSubcategoryView

urlpatterns = [
    path("v1/category/", CreateCategoryOrSubcategoryView.as_view()),
    path("v1/category/<int:pk>/", CreateCategoryOrSubcategoryView.as_view()),
    # path("v1/get-top-level-category/", GetTopcategoryView.as_view()),
    # path("v1/organization/", OrganizationView.as_view()),
    # path("v1/type_of_employee/", TypeOfEmployeeView.as_view()),
    # path("v1/organization/<int:pk>/", OrganizationView.as_view()),
    ]
