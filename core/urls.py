"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Custom "Caesar" Admin Header Customization
admin.site.site_header = "Sanaa-Sync: Caesar Admin" # Large text at the top
admin.site.site_title = "Caesar Portal"             # Browser Tab title
admin.site.index_title = "Swahilipot Creatives Dept." # Main subtitle

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')), # This handles the home page and future account URLs
    # Later we will add:
    # path('booking/', include('resources.urls')),

]
