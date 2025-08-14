from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.user_list, name='user_list'),
    path("post/", views.create_post, name="post"),
    path("profile/", views.profile_view, name="profile_view"),
    path("add_friend/<int:user_id>", views.add_friend, name="add_friend"),
    path("remove_friend/<int:user_id>", views.remove_friend, name="remove_friend"),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]