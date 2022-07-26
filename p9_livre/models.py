from django.urls import reverse
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from PIL import Image


class Ticket(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True, null=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField()
    validators = [MinValueValidator(0), MaxValueValidator(5)]
    likes = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='likes_tickets')



    def resize_image(self):
        print("self")
        print(self)
        print(self.image)
        image = Image.open(self.image) 

        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def get_absolute_url(self):
        return reverse('Home')


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.CharField(max_length=128)

    description = models.TextField(max_length=2048, blank=True, null=True)
    rating = models.PositiveSmallIntegerField()
    # validates that rating must be between 0 and 5
    validators = [MinValueValidator(0), MaxValueValidator(5)]
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='likes_reviews')


    def get_absolute_url(self):
        return reverse('Home')


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )
