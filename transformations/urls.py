from django.urls import path
from .views import highlight, index

urlpatterns = [
    path('', index, name='index'),
    path('highlight', highlight, name='highlight'),
]
