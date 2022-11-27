from django.urls import path
from .views import  *

urlpatterns = [
    path('create/', Create.as_view()),
]