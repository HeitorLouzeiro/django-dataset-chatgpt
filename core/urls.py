from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('question/<int:id>', views.question, name='question'),
    path('createPrompt/<int:id>', views.createPrompt, name='createPrompt'),
    path('editPrompt/<int:id>/<int:prompt_id>',
         views.editPrompt, name='editPrompt'),
    path('deletePrompt/<int:id>/<int:prompt_id>',
         views.deletePrompt, name='deletePrompt'),
    path('query/<int:id>', views.query, name='query'),
    path('delete/<int:id>', views.delete, name='delete'),
]
