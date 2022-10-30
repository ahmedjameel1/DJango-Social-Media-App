from django.db.models import Q
from profiles.models import *
from accounts.models import * 

def searchAll(request):

    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    posts = Post.objects.filter(Q(text__icontains=search_query))
    posts = list(posts)
    for post in posts:
        if post.owner == request.user.profile:
            posts.remove(post)
    print(posts)
    pages = Page.objects.distinct().filter(Q(title__iexact=search_query)|Q(category__iexact=search_query))
    users = Profile.objects.filter(name__iexact=search_query)
    return posts,pages,users,search_query