from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('<int:id>', views.group_view, name='group'),
    path('todo/', views.group_list,name='group_api'),
]