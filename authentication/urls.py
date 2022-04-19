from django.urls import path, include
from authentication import views

urlpatterns = [
    path('login/',views.loginuser,name='login'),
    path('register/',views.signup, name='register'),
    path('logout/',views.logoutuser,name='logout'),
    path('activate_user/<useridb64>/<token>',views.activate_user,name='activate'),
    path('set-new-password/<useridb64>/<token>',views.SetNewPassword,name='set-new-password'),
    path('resetpassword/', views.RequestResetPassword , name='resetpassword'),
    path('editprofile/', views.editprofile , name='editprofile'),
]