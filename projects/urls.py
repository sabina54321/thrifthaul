# from ast import pattern
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    
    path('login/', views.loginUser, name='login'),
    # path('logout/', views.logoutUser, name='logout'),

    path('Register/', views.Register, name='Register'),

    path('Sell/', views.Sell, name='Sell'),

     path('logout/', views.logoutUser, name='logout'),

    path('productdetail/', views.productdetail , name='productdetail'),

    path('products/', views.products , name='products'),

]
