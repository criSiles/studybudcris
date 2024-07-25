from django.urls import path 
# urls and views are in the same directory so we're going to import the views to access the functions to route
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logut/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
]
