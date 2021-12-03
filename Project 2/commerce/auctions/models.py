from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

active_status_id = 1 #id of the "active" object of the the Status model

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    amount = models.IntegerField(default=10)
    bidder = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"current bid: ${self.amount} by {self.bidder}."

class Status(models.Model):
    status = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.status}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512, null=True)
    url = models.URLField(blank=True, null=True)
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE, primary_key=True)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(Category, related_name="category_items", on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="listings", default=1)

    def __str__(self):
        return f"{self.title} posted by {self.lister}: Current bid is ${self.bid.amount}."

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=256)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments_on_listing")

    def __str__(self):
        return f"{self.commenter}:   {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist", null=True)
    listing = models.ManyToManyField(Listing, related_name="watchlisted_items")

    def __str__(self):
        return f"{self.listing}"