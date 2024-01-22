from django.urls import path
from .views import edit_1, edit_2, highlight, index

urlpatterns = [
    path('', index, name='index'),
    path('edit_1', edit_1, name='edit_1'),
    path('edit_2', edit_2, name='edit_2'),
    path('highlight', highlight, name='highlight'),
]
