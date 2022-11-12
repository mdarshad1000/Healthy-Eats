from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('upload_and_extract/', views.upload_and_extract, name='upload-and-extract'),
    path('nutrition/', views.nutrition, name='nutrition'),
    path('recipe/', views.recipe, name='recipe')
]