# from ast import pattern
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('Sell/', views.Sell, name='Sell'),
    path('productdetail/<int:id>', views.productdetail , name='productdetail'),
    path('products/', views.products , name='products'),
    path('search/', views.search , name='search'),
    path('profile/', views.profile , name='profile'),
    path('productdelete/<int:id>', views.deleteproduct, name='productdelete'),
] 