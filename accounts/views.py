from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import HubSignUpForm, UserUpdateForm
from resources.models import GigApplication, SuccessStory, Resource

@login_required
def profile_view(request):
    # Added vetting status context to help the profile page show the right badge
    my_applications = GigApplication.objects.filter(artist=request.user).select_related('gig').order_by('-applied_on')
    
    context = {
        'applications': my_applications,
        'is_vetted': request.user.is_vetted, # Explicitly passing this for the badge logic
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile_view')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

# --- 1. The Landing Page (The "Artist Showcase") ---
def landing_page(request):
    # Fetch Success Stories
    success_stories = SuccessStory.objects.all().order_by('-created_at')
    
    # Fetch Equipment (Resource type 'gear' or 'instrument')
    equipment = Resource.objects.filter(
        resource_type__in=['gear', 'instrument'], 
        status='available'
    )[:6] 
    
    # Fetch Halls (Resource type 'hall')
    halls = Resource.objects.filter(
        resource_type='hall', 
        status='available'
    )
    
    context = {
        'success_stories': success_stories,
        'equipment': equipment,
        'halls': halls,
        'page_title': 'Sanaa-Sync V2 | Home'
    }
    
    return render(request, 'accounts/landing.html', context)

# --- 2. The Talent Directory (ONLY SHOWS VERIFIED) ---
def talent_directory(request):
    """
    Public directory that only displays vetted artists to ensure 
    high-quality representation of the Hub.
    """
    # STAGE 2: Filter logic strictly ensures only is_vetted=True artists appear
    vetted_artists = User.objects.filter(is_vetted=True, role='creative').order_by('-date_joined')
    
    # Simple search integration if needed later
    search_query = request.GET.get('search')
    if search_query:
        vetted_artists = vetted_artists.filter(full_name__icontains=search_query)

    return render(request, 'accounts/talent_directory.html', {
        'artists': vetted_artists,
        'page_title': 'Verified Hub Talent'
    })

# --- 3. The Success Story Detail Page ---
def story_detail(request, story_id):
    story = get_object_or_404(SuccessStory, pk=story_id)
    return render(request, 'accounts/story_detail.html', {'story': story, 'page_title': f"{story.artist_name} | Story Detail"})

# --- 4. The Signup Logic ---
def signup(request):
    if request.method == 'POST':
        form = HubSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'creative'
            # New users start unvetted by default
            user.is_vetted = False 
            user.save()
             
            login(request, user)
            messages.info(request, "Welcome! Complete your portfolio to get your 'Vetted' badge.")
            return redirect('profile_view') 
    else:
        form = HubSignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})