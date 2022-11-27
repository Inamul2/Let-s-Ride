from django.urls import path
from .views import  *

urlpatterns = [
    path('request/', Request.as_view()),
    path('getRequests/', GetRequests.as_view()),
    path('getMatchedRequests/', GetMatchedRequests.as_view()),
    path('apply/', Apply.as_view()),
]