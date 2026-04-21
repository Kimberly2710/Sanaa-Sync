from django.urls import path
from django.contrib.auth import views as auth_views # Import Django's built-in auth
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('join-hub/', views.signup, name='join_hub'),
    
    # Built-in Login/Logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
]