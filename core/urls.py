from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Custom "Caesar" Admin Header Customization
admin.site.site_header = "Sanaa-Sync: Swahilipot Admin"
admin.site.site_title = "Caesar Portal"
admin.site.index_title = "Swahilipot Creatives Dept."

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This pulls in everything from accounts/urls.py
    path('', include('accounts.urls')),   
    
    # This pulls in everything from resources/urls.py (Gigs, Bookings)
    path('', include('resources.urls')),  

    # Global Logout path
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
]