from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Gig, GigApplication, Resource, Booking, BookingItem
from .forms import BookingForm, GigApplicationForm

# --- GALLERY VIEWS FOR NAVBAR ---

def equipment_list(request):
    """View only gear and instruments with search/filter"""
    resources = Resource.objects.filter(resource_type__in=['gear', 'instrument'], status='available')
    
    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    
    if category_filter:
        resources = resources.filter(resource_type=category_filter)
    
    if search_query:
        resources = resources.filter(name__icontains=search_query) | resources.filter(description__icontains=search_query)
    
    return render(request, 'resources/resource_list.html', {
        'resources': resources, 
        'title': 'Equipment & Gear',
        'search_query': search_query,
        'category_filter': category_filter
    })

def halls_list(request):
    """View only spaces/halls with search"""
    resources = Resource.objects.filter(resource_type='hall', status='available')
    
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        resources = resources.filter(name__icontains=search_query) | resources.filter(description__icontains=search_query)
    
    return render(request, 'resources/resource_list.html', {
        'resources': resources, 
        'title': 'Halls & Spaces',
        'search_query': search_query
    })

# --- MULTI-ITEM BOOKING LOGIC ---

@login_required
def book_multiple(request):
    """The 'Master Form' to book many items at once"""
    # We fetch all available resources to display them in the form
    all_resources = Resource.objects.filter(status='available')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # 1. Create the Main Booking Header
            booking = form.save(commit=False)
            booking.user = request.user
            
            # Simple Time Validation
            if booking.start_time >= booking.end_time:
                messages.error(request, "End time must be after start time.")
                return render(request, 'resources/booking_master_form.html', {'form': form, 'resources': all_resources})

            # 2. Extract quantities from the POST data
            items_to_create = []
            for resource in all_resources:
                qty_input = request.POST.get(f'qty_{resource.id}', 0)
                
                # If they wrote "N/A" or left it blank/0, we skip it
                try:
                    qty = int(qty_input)
                except (ValueError, TypeError):
                    qty = 0
                
                if qty > 0:
                    # CHECK AVAILABILITY: See how many are already booked for this time
                    already_booked = BookingItem.objects.filter(
                        resource=resource,
                        booking__status__in=['pending', 'approved'],
                        booking__start_time__lt=booking.end_time,
                        booking__end_time__gt=booking.start_time
                    ).aggregate(Sum('quantity_requested'))['quantity_requested__sum'] or 0
                    
                    if (already_booked + qty) > resource.quantity:
                        messages.error(request, f"Sorry, only {resource.quantity - already_booked} units of {resource.name} are available for this time.")
                        return render(request, 'resources/booking_master_form.html', {'form': form, 'resources': all_resources})
                    
                    # Prepare the item for saving
                    items_to_create.append(BookingItem(resource=resource, quantity_requested=qty))

            if not items_to_create:
                messages.error(request, "You didn't select any items to book.")
                return render(request, 'resources/booking_master_form.html', {'form': form, 'resources': all_resources})

            # 3. Everything is valid -> SAVE
            booking.save()
            for item in items_to_create:
                item.booking = booking
                item.save()
            
            messages.success(request, "Master booking submitted! Wait for admin approval.")
            return redirect('halls_list')

    else:
        form = BookingForm()
    
    return render(request, 'resources/booking_master_form.html', {
        'form': form, 
        'resources': all_resources
    })

# --- GIG LOGIC (Keep as is) ---
def gig_list(request):
    active_gigs = Gig.objects.filter(is_open=True).order_by('event_date')
    return render(request, 'resources/gig_list.html', {'gigs': active_gigs})

@login_required
def apply_for_gig(request, gig_id):
    gig = get_object_or_404(Gig, id=gig_id)
    if request.method == 'POST':
        if not request.user.is_vetted:
            messages.warning(request, "Profile must be vetted to apply.")
            return redirect('gig_list')
        form = GigApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.gig = gig
            application.artist = request.user
            application.save()
            messages.success(request, f"Application for {gig.title} sent.")
            return redirect('profile')
    else:
        form = GigApplicationForm()
    return render(request, 'resources/apply_confirm.html', {'gig': gig, 'form': form})

# --- MY BOOKINGS LOGIC ---

@login_required
def my_bookings(request):
    """View to list bookings made by the current user."""
    # Pre-fetch items and their associated resource to prevent N+1 queries
    bookings = Booking.objects.filter(user=request.user).order_by('-start_time').prefetch_related('items__resource')
    return render(request, 'resources/my_bookings.html', {'bookings': bookings})

@login_required
def delete_booking(request, booking_id):
    """View to allow users to cancel/delete their own bookings."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        # Ensure only pending or certain bookings can be cancelled, or just allow deletion.
        # It's safer to delete or set status to cancelled. We'll simply delete it per user request.
        booking.delete()
        messages.success(request, "Booking successfully deleted.")
        return redirect('my_bookings')
        
    return redirect('my_bookings')