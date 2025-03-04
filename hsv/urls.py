

# Create your views here.
from django.urls import path, include
from . import views 
from .views import listing


urlpatterns = [ 
path('',views.home, name='home',),
path('property',views.property, name='property'),
path('about',views.about, name='about'),
path('contact',views.contact, name='contact'),
path('property-listings/<slug:slug>/', listing, name='property_detail'),
path('privacy',views.privacy, name='privacy'),
path('faq',views.faq, name='faq'),



]