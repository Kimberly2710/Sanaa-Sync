from django.db import models
from django.conf import settings
from django.utils.text import slugify

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
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
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
        return f"{self.resource.name} | {self.user.username} | {self.start_time.strftime('%d %b')}"

# --- NEW GIG & MARKETPLACE LOGIC ---

class Gig(models.Model):
    """Opportunities for artists to apply for events/work"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255, default="Swahilipot Hub")
    slots_available = models.IntegerField(default=1)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class GigApplication(models.Model):
    """The link between an Artist and a Gig"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )

    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='applications')
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gig_applications')
    message = models.TextField(help_text="Why should you get this gig?")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist.username} -> {self.gig.title}"


class SuccessStory(models.Model):
    """Success stories showcasing artist achievements"""
    artist_name = models.CharField(max_length=200, help_text="Name of the artist")
    story = models.TextField(help_text="The success story text")
    image = models.ImageField(upload_to='success_stories/', help_text="Artist image or story image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=True, help_text="Show on landing page")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.artist_name} - Success Story"