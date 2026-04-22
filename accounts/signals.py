from resources.models import Gig
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User
import logging

# Set up logging so you can see errors in your terminal
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def send_vetting_notification(sender, instance, created, **kwargs):
    """
    Triggered when a User is saved. Sends email only if is_vetted becomes True.
    """
    # Logic: If it's not a new user (update) and they are now vetted
    if not created and instance.is_vetted:
        try:
            subject = "Verified: Your Sanaa-Sync Artist Badge is Active!"
            message = f"""
            Hi {instance.username},

            The Swahilipot Creatives Dept has officially VETTED your profile! 

            You now have full access to:
            - Exclusive Gig Applications
            - The Public Talent Directory
            - Your 'Verified' Profile Badge

            Log in to the Caesar Portal to see what's new:
            {settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'}

            Keep building the ecosystem,
            Swahilipot Hub Admin
            """
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
            )
            print(f" Success: Vetting email sent to {instance.username}")
            
        except Exception as e:
            # As an App Admin, you want to know WHY an email failed without crashing the site
            logger.error(f" Email Failed for {instance.username}: {e}")

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Sends a welcome email immediately after a successful 'Join Hub' signup.
    """
    if created:
        try:
            subject = "Welcome to the Swahilipot Hub Creative Community!"
            message = f"""
            Karibu, {instance.username}!

            Thank you for joining Sanaa-Sync. Your journey as a Hub Creative starts now.

            Next Steps:
            1. Complete your profile bio and portfolio.
            2. Wait for the Dept to review and 'Vet' your account.
            3. Once vetted, you can start applying for Gigs!

            We are excited to see what you create.
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f" Welcome email failed for {instance.username}: {e}")



@receiver(post_save, sender=Gig)
def notify_artists_of_new_gig(sender, instance, created, **kwargs):
    """
    When a new Gig is created and is_open=True, notify all vetted artists.
    """
    if created and instance.is_open:
        # Get only the emails of artists who have been vetted by the Dept
        from accounts.models import User

        recipient_list = User.objects.filter(
            is_vetted=True, 
            is_active=True
        ).values_list('email', flat=True)

        if recipient_list:
            try:
                subject = f"NEW GIG: {instance.title} at Swahilipot Hub"
                message = f"""
                Hi Creative,

                A new opportunity has just been posted on Sanaa-Sync!

                Gig: {instance.title}
                Date: {instance.event_date}
                Description: {instance.description[:100]}...

                Log in to the Caesar Portal to apply now:
                {settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'}/gigs/

                Don't miss out!
                Swahilipot Creatives Dept.
                """
                
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    list(recipient_list),
                    fail_silently=False,
                )
                print(f" Gig Alert sent to {len(recipient_list)} vetted artists.")
            except Exception as e:
                logger.error(f" Gig Alert failed: {e}")
