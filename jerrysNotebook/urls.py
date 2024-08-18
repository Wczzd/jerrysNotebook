from django.urls import path
from . import views

app_name = 'jerrysNotebook'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>', views.topic, name='topic'),
    path('newTopic/', views.newTopic, name='newTopic'),
    path('newEntry/<int:topic_id>/', views.newEntry, name='newEntry'),
    path('newComment/<int:entry_id>/', views.editEntry, name='editEntry'),
]