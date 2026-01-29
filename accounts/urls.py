
from django.urls import path
from .views import index, register_view, login_view, logout_view, profile_view, edit_profile_view, toggle_like, add_comment, follow_toggle, users_list

urlpatterns = [
    path('', index, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('like/<int:post_id>/', toggle_like, name='toggle_like'),
    path('comment/<int:post_id>/', add_comment, name='add_comment'),
    path('follow/<str:username>/', follow_toggle, name='follow_toggle'),
    path('users/', users_list, name='users'),


]

