from django.shortcuts import render
from .models import User, ArtistSkill

def landing_page(request):
    # Fetch all vetted artists to show on the home page
    vetted_artists = User.objects.filter(role='creative', is_vetted=True).prefetch_related('skills')
    
    context = {
        'artists': vetted_artists,
        'page_title': "Sanaa-Sync | Creative Directory"
    }
    return render(request, 'accounts/landing.html', context)