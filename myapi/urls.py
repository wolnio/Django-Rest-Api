from django.urls import path, include
from . import views

urlpatterns = [
    path('cars/', views.car_list),
    path('cars/<int:pk>', views.car_detail),
    path('cars/rate', views.car_rate)
]
