from django.urls import path, include
from authentication import views

urlpatterns = [
    path('login/',views.loginuser,name='login'),
    path('register/',views.signup, name='register'),
    path('logout/',views.logoutuser,name='logout'),
    path('activate_user/<useridb64>/<token>',views.activate_user,name='activate'),
    # path('activate_user/<useridb64>/<token>',views.activate_user,name='activate'),
    path('editprofile/', views.editprofile , name='editprofile'),
]