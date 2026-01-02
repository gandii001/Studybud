from . import views
from django.urls import include, path


urlpatterns = [
    path('', views.Home, name ='Home'),
    path('room/<str:pk>/', views.room, name = 'room'),  #/<str:pk>/ this is a dynamic routing,pk is a primary key
    path('create_room/', views.createRoom, name = 'create_room'),
    path('update-room/<str:pk>/', views.updateRoom, name = 'update-room'),
    path('user-profile/<str:pk>/', views.userProfile, name = 'user-profile'),
    path('delete-room/<str:pk>/', views.deleteRoom, name = 'delete-room'),
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('signup/', views.registerUser, name = 'signup'),
    path('deleteMessage/<str:pk>/', views.deleteMessage, name = 'deleteMessage'),
    path('updateUser/', views.updateUser, name = 'updateUser'),
    path('topicsPage/', views.topicsPage, name = 'topicsPage'),
    path('activityPage/', views.activityPage, name = 'activityPage'),
] 
