# from ast import pattern
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('Sell/', views.Sell, name='Sell'),
    path('productdetail/<int:id>', views.productdetail , name='productdetail'),
    path('products/', views.products , name='products'),
    path('search/', views.search , name='search'),
    path('profile/', views.profile , name='profile'),
    path('buyerviewprofile/<int:id>', views.buyerviewprofile , name='buyerviewprofile'),
    path('productdelete/<int:id>', views.deleteproduct, name='productdelete'),
    path('confirmdelete/<int:id>', views.confirmdelete , name='confirmdelete'),
    path('submitreview/<int:id>', views.submitreview, name='submitreview'),
    path('editproduct/<int:id>', views.editproduct , name='editproduct'),
] 