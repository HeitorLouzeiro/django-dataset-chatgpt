from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('question/<int:id>', views.question, name='question'),
    path('query/<int:id>', views.query, name='query'),
    path('delete/<int:id>', views.delete, name='delete'),
]
