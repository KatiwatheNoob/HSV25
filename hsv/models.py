from django.db import models
import datetime
from tinymce.models import HTMLField
from django.utils.text import slugify
from cloudinary.models import CloudinaryField




# Create your models here.

class Property(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)  # Automatically generated
    mainImage = CloudinaryField('image')  # ✅ Store in Cloudinary
    briefDescription = models.TextField(max_length=500)
    details = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    sellingSize = models.CharField(max_length=10, default=1, blank=True)
    longDescription = models.TextField(max_length=500, blank=True)
    amount = models.IntegerField(default=0)

    @property
    def formatted_amount(self):
        return "{:,}".format(self.amount)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1

            while Property.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug  # Ensures unique slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Properties'

# ✅ Fixed Image Model
class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')  # ✅ Store in Cloudinary

    def __str__(self):
        return f"Image for {self.property.name}"


from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

