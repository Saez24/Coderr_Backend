from django.db import models
from profile_app.models import Profile


class OfferDetail(models.Model):
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(null=True, blank=True)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    features = models.JSONField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)


class Offer(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE,  blank=True, null=True, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile_pictures/', null=True, )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = models.JSONField(default=list)
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    max_delivery_time = models.IntegerField(null=True, blank=True)
    min_delivery_time = models.IntegerField(null=True, blank=True)
    user_details = models.JSONField(default=list, blank=True)
