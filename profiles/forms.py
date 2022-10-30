from django import forms 
from .models import Comment, Post, Photo, Video, Page, Message

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text','image',)

   
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('name','image',)

    
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('name','video',)

   

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title','image','category')

   

class PagePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text','image')

    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject','body')
    
    