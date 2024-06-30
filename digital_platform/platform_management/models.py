from django.db import models
from user_management.models import User
import uuid



# Create your models here.
class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    postalCode = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class AddressUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    postalCode = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    announcement = models.TextField()

    def __str__(self):
        return self.name
    

class Forum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)
    problem = models.TextField()

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    comment = models.TextField()


class LostAndFound(models.Model):

    TYPE = (
        ("L", "LOST"),
        ("F", "FOUND")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    createdAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    type = models.CharField(choices=TYPE, default='L')
    picture = models.ImageField(upload_to="uploads/", null=True, blank=True)
    desc = models.TextField()

    def __str__(self):
        return self.name