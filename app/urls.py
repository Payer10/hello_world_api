from django.urls import path

from .views import *

urlpatterns = [
    path("subcontinents/", subcontinent_list_create, name="subcontinent-list"),
    path("subcontinents/<int:pk>/", subcontinent_detail, name="subcontinent-detail"),

    path("countries/", country_list_create, name="country-list"),
    path("countries/<int:pk>/", country_detail, name="country-detail"),

    path("dishes/", dish_list_create, name="dish-list"),
    path("dishes/<int:pk>/", dish_detail, name="dish-detail"),
]