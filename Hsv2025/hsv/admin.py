from django.contrib import admin
from .models import Property,Image, ContactMessage
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image
    extra = 6 # Number of extra fields to add images in the admin panel

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    formfield_overrides = {
    models.TextField: {'widget': TinyMCE()},
    }

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "sent_at")
    search_fields = ("name", "email", "subject")   

admin.site.register(Property, PropertyAdmin)