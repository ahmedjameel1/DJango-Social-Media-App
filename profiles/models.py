from django.db import models
from accounts.models import Profile , Account
import uuid

# Create your models here.

class Like(models.Model):
    page = models.ForeignKey('Page',blank=True,null=True, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', blank=True,null=True,on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.owner.username
    

class Comment(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.username


class Post(models.Model):
    page = models.ForeignKey('Page',blank=True,null=True, on_delete=models.CASCADE)
    image = models.ImageField(default=None,upload_to="posts/%y/%m/%d",null=True, blank=True)
    text = models.TextField(max_length=255)
    owner = models.ForeignKey(Profile, blank=True,null=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.text)


    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'None'
        return url


class Photo(models.Model):
    page = models.ForeignKey('Page',blank=True,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True, blank=True)
    image = models.ImageField(default=None,upload_to="photos/%y/%m/%d",null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    page = models.ForeignKey('Page',blank=True,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True, blank=True)
    video= models.FileField(upload_to='videos//%y/%m/%d', null=True)    
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    owner = models.ForeignKey(Account, blank=True, null=True,on_delete=models.CASCADE)
    location = models.CharField(max_length=50,null=True, blank=True)
    category = models.CharField(max_length=100,null=True,blank=True)
    title = models.CharField(max_length=50,null=True, blank=True)
    image = models.ImageField(default=None,upload_to="pages/%y/%m/%d",null=True, blank=True)
    subscribers = models.ManyToManyField(Profile,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'None'
        return url


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True , blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True , blank=True, related_name="messages")
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    is_read = models.BooleanField(default=False,null=True)
    body = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read','-created']