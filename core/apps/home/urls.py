from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register, name='register'),
    path('delete_recipe/<id>/', views.delete_recipe, name='delete_recipe'),
    path('update_recipe/<id>/', views.update_recipe, name='update_recipe')
]
