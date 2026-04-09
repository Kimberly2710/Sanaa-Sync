from django.contrib import admin
from .models import Resource, Booking, Gig, GigApplication, SuccessStory

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    # Live-typing slugs makes the UI feel "Swiss-modern" and fast
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'resource_type', 'status', 'quantity', 'capacity')
    list_filter = ('resource_type', 'status')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'start_time', 'status', 'assigned_staff')
    list_filter = ('status', 'start_time')
    date_hierarchy = 'start_time' # Adds a nice timeline filter at the top

# --- NEW: Marketplace Admin ---

class GigApplicationInline(admin.TabularInline):
    """Allows the Admin to see applicants directly inside the Gig page"""
    model = GigApplication
    extra = 0
    readonly_fields = ('applied_on',)

@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'slots_available', 'is_open', 'applicant_count')
    list_filter = ('is_open', 'event_date')
    search_fields = ('title', 'description')
    inlines = [GigApplicationInline]

    def applicant_count(self, obj):
        return obj.applications.count()
    applicant_count.short_description = "Applicants"

@admin.register(GigApplication)
class GigApplicationAdmin(admin.ModelAdmin):
    list_display = ('artist', 'gig', 'status', 'applied_on')
    list_filter = ('status', 'applied_on')
    # Use autocomplete to handle large numbers of artists/gigs
    autocomplete_fields = ['artist', 'gig']

@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('artist_name', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('artist_name', 'story')
    readonly_fields = ('created_at', 'updated_at')