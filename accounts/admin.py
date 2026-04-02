from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, ArtistSkill

# 1. Customizing how Users are displayed for the Creative Admin
class UserAdmin(BaseUserAdmin):
    """
    Standard UserAdmin doesn't know about our custom fields (role, vetted).
    We must explicitly add them to the fieldsets.
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'age', 'bio')}),
        ('Creative Status', {'fields': ('role', 'is_vetted', 'is_hub_staff')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # These columns will be visible in the User List view
    list_display = ('username', 'email', 'first_name', 'role', 'is_vetted', 'is_staff')
    
    # Allow filtering by these fields on the right side
    list_filter = ('role', 'is_vetted', 'is_hub_staff', 'date_joined')
    
    # Set 'creative' as the default view for the Dept. Head
    ordering = ('-date_joined',)

# 2. Make the skill mapping editable right from the User page
class ArtistSkillInline(admin.TabularInline):
    """Allows adding Primary/Secondary arts directly while creating a user."""
    model = ArtistSkill
    extra = 1 # Shows one blank row by default

# 3. Apply the skill inline to the UserAdmin
UserAdmin.inlines = [ArtistSkillInline]

# 4. A clean view for Category (e.g., Dancers, Poets)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# 5. Register the User model with our custom Admin class
admin.site.register(User, UserAdmin)