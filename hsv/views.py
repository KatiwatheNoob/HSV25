from django.shortcuts import render
from .models import Property,ContactMessage
from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging
import requests
from django.conf import settings
import random
import time


# Initialize Logger
logger = logging.getLogger(__name__)

def home(request):
    properties = Property.objects.all()
    
    return render (request,'index.html',{'properties':properties})  


def property(request):
    properties = Property.objects.all()

    for prop in properties:  # Avoid variable shadowing
        default_image = prop.images.first()  # Use related_name "images"
        prop.default_image_url = default_image.image.url if default_image else 'path/to/default/image.jpg'

    return render(request, 'property.html', {'properties': properties})


def contact(request):
    if request.method == 'POST':
        message_name = request.POST.get('message_name', '').strip()
        message_email = request.POST.get('message_email', '').strip()
        message_subject = request.POST.get('message_subject', '').strip()
        message = request.POST.get('message', '').strip()
        recaptcha_response = request.POST.get('g-recaptcha-response')


          # Save the message to the database
        ContactMessage.objects.create(
            name=message_name,
            email=message_email,
            subject=message_subject,
            message=message
        )

        # Introduce a small delay to slow down bots
        time.sleep(random.uniform(0.5, 1.5))

        # Validate Email
        try:
            validate_email(message_email)
        except ValidationError:
            return render(request, 'contact.html', {'error': 'Invalid email address'})

        # Check Empty Fields
        if not (message_name and message_email and message_subject and message):
            return render(request, 'contact.html', {'error': 'All fields are required'})

        # Verify Google reCAPTCHA
        recaptcha_secret = settings.RECAPTCHA_SECRET_KEY
        recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
        recaptcha_data = {'secret': recaptcha_secret, 'response': recaptcha_response}
        recaptcha_result = requests.post(recaptcha_verify_url, data=recaptcha_data).json()

        if not recaptcha_result.get("success"):
            return render(request, 'contact.html', {'error': 'reCAPTCHA failed. Try again!'})

        try:

            
            # Send Email
            send_mail(
                subject=message_subject,
                message=f"Name: {message_name}\nEmail: {message_email}\n\n{message}",
                from_email='no-reply@hindsight-ventures.com',
                recipient_list=['roykatiwa@hindsight-ventures.com'],
                fail_silently=False,
            )
            return render(request, 'contact.html', {'success': 'Message sent successfully!'})
        except Exception as e:
            logger.error(f"Email Sending Failed: {e}")
            return render(request, 'contact.html', {'error': 'Error sending email. Try again later.'})

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
def privacy(request):
    return render(request, 'privacy.html')
def faq(request):
    return render(request, 'faq.html')


def listing(request, slug):
    # Get the property based on the slug
    active_property = get_object_or_404(Property, slug=slug)

    # Ensure images exist before accessing them
    images = active_property.images.all() if hasattr(active_property, 'images') else []

    # Get similar properties by location (not by ID!)
    similar_properties = Property.objects.filter(location=active_property.location).exclude(id=active_property.id)[:3]

    # Handle default image if no images exist
    main_image_url = images[0].image.url if images else 'path/to/default/image.jpg'

    return render(request, 'listing.html', {
        'property': active_property,
        'similar_properties': similar_properties,
        'property_images': images,
        'main_image_url': main_image_url
    })

