from django.db import models
from django.conf import settings
from django.utils.text import slugify
from cloudinary.models import CloudinaryField # Required for resource images

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('hall', 'Space/Hall'),
        ('gear', 'Equipment/Gear'),
        ('instrument', 'Musical Instrument'),
    )

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired/Broken'),
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    resource_type = models.CharField(max_length=15, choices=RESOURCE_TYPES)
    # Added Image Field for the resource gallery
    image = CloudinaryField('resource_image', null=True, blank=True) 
    description = models.TextField(blank=True)
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    capacity = models.IntegerField(default=0, help_text="Applicable for Halls")
    quantity = models.IntegerField(default=1, help_text="Number of units available")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"


class Booking(models.Model):
    """
    This acts as the 'Header'. 
    A user creates one Booking that can contain many items.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    # Use a generic name for the booking session (e.g., "Mics and Hall for Rehearsal")
    event_title = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='supervised_sessions'
    )

    def __str__(self):
        return f"{self.event_title or 'Booking'} | {self.user.username} | {self.start_time.strftime('%d %b')}"

class BookingItem(models.Model):
    """
    This links multiple resources to a single booking.
    When the user fills the 'Master Form', we create one BookingItem for each resource.
    """
    booking = models.ForeignKey(Booking, related_name='items', on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity_requested} x {self.resource.name} for {self.booking}"


# --- GIG & SUCCESS STORIES REMAIN THE SAME ---

class Gig(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255, default="Swahilipot Hub")
    slots_available = models.IntegerField(default=1)
    is_open = models.BooleanField(default=True)
    requirements = models.TextField(help_text="What skills or gear do they need?", blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in KES", default=0.00)

    def __str__(self):
        return self.title

class GigApplication(models.Model):
    STATUS_CHOICES = (('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined'))
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='applications')
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gig_applications')
    message = models.TextField(blank=True)
    voice_message = models.FileField(upload_to='voice_messages/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist.username} -> {self.gig.title}"

class SuccessStory(models.Model):
    artist_name = models.CharField(max_length=200)
    story = models.TextField()
    image = CloudinaryField('success_story_image', null=True, blank=True) # Switched to Cloudinary
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.artist_name} - Success Story"