from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    """Departments: Dancers, Poets, Fashion, Film, etc."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class User(AbstractUser):
    """Custom User for Swahilipot Hub Creatives"""
    ROLE_CHOICES = (
        ('admin', 'Creative Admin'),
        ('creative', 'Creative/Artist'),
        ('client', 'Partner/Supplier'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='creative')
    phone_number = models.CharField(max_length=15, blank=True)
    is_vetted = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True) # Targeting 18-25
    is_hub_staff = models.BooleanField(default=False) # True for Interns/Staff on the roster
    
    def __str__(self):
        return f"{self.username} ({self.role})"

class ArtistSkill(models.Model):
    """Links Artists to their Arts with Priority Logic"""
    PRIORITY_CHOICES = (
        ('primary', 'Primary Art'),
        ('secondary', 'Secondary Art'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='secondary')
    years_experience = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'category') # Prevents duplicate entries for same category

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.priority})"