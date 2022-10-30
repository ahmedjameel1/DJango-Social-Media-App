from django.shortcuts import render
from django.http import HttpResponse
from profiles.models import Post, Page
from django.contrib.auth.decorators import login_required
from itertools import chain
from accounts.models import Profile
from profiles.utils import searchAll
# Create your views here.

@login_required(login_url="login")
def home(request):
    if request.user.is_authenticated:
        posts,pages,users,search_query = searchAll(request)
    ctx = {'posts': posts,'users': users,'pages': pages}
    return render(request,'home/home.html',ctx)
