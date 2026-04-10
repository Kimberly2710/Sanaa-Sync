from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Added for user feedback
from .models import Gig, GigApplication, Resource, Booking
from .forms import BookingForm

def gig_list(request):
    # Only show gigs that are currently open for applications
    active_gigs = Gig.objects.filter(is_open=True).order_by('event_date')
    return render(request, 'resources/gig_list.html', {'gigs': active_gigs})

@login_required # Only logged-in artists can apply
def apply_for_gig(request, gig_id):
    gig = get_object_or_404(Gig, id=gig_id)
    
    # --- THE VETTING GATE (BACKEND SECURITY) ---
    if not request.user.is_vetted:
        messages.warning(request, f"Access Denied. Your profile must be vetted to apply for '{gig.title}'.")
        return redirect('gig_list')
    
    if request.method == 'POST':
        # Check if they already applied to prevent double submissions
        already_applied = GigApplication.objects.filter(gig=gig, artist=request.user).exists()
        
        if already_applied:
            messages.info(request, "You have already submitted an application for this gig.")
            return redirect('profile')

        # Create the application linked to the logged-in user
        GigApplication.objects.create(
            gig=gig,
            artist=request.user,
            message=request.POST.get('message', '')
        )
        
        messages.success(request, f"Success! Your application for {gig.title} has been sent.")
        return redirect('profile') # Redirect to profile to see the application status
    
    return render(request, 'resources/apply_confirm.html', {'gig': gig})

def resource_list(request):
    """View available spaces, equipment, and instruments."""
    resources = Resource.objects.filter(status='available')
    return render(request, 'resources/resource_list.html', {'resources': resources})

@login_required
def book_resource(request, resource_id):
    """Handle booking of a specific resource."""
    resource = get_object_or_404(Resource, id=resource_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.resource = resource
            
            if booking.start_time >= booking.end_time:
                messages.error(request, "End time must be after start time.")
            else:
                # Check for overlapping bookings
                overlapping = Booking.objects.filter(
                    resource=resource,
                    status__in=['pending', 'approved'],
                    start_time__lt=booking.end_time,
                    end_time__gt=booking.start_time
                ).exists()
                
                if overlapping:
                    messages.error(request, "This resource is already booked for the selected time.")
                else:
                    booking.save()
                    messages.success(request, f"Your booking for {resource.name} is submitted and pending approval.")
                    return redirect('resource_list')
    else:
        form = BookingForm()
        
    return render(request, 'resources/booking_form.html', {'form': form, 'resource': resource})