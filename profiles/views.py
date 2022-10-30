from django.shortcuts import render , redirect
from accounts.models import Profile, FriendRequests
from accounts.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from profiles.models import Post, Like , Comment, Photo, Video , Page, Message
from .forms import CommentForm, PostForm, PhotoForm, VideoForm, PageForm, PagePostForm, MessageForm
from django.contrib import messages
from .utils import searchAll
from django.http import HttpResponse


# Create your views here.

@login_required(login_url='login')
def singleprofile(request,pk):
    profile = Profile.objects.get(id=pk)
    posts = Post.objects.filter(owner=profile).order_by('-created_at')
    print(posts)
    current_profile = request.user.profile
    try:
        friends_list = list(current_profile.friends.all())
        if profile in friends_list:
            afriend = True
        else:
            afriend = False
    except:
        pass
    try:
        requestexists = FriendRequests.objects.filter(sender=request.user,reciever=profile).exists()
        if requestexists:
            requestexists = True
        else:
            requestexists = False
    except:
        pass
    ctx = {'profile': profile,'posts':posts,'afriend':afriend,'requestexists':requestexists}
    return render(request, 'profiles/singleprofile.html',ctx)

@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('singleprofile', profile.id)
    else:
        form = ProfileForm(instance=profile)
    ctx = {'form': form}
    return render(request, 'profiles/profileform.html',ctx)

@login_required(login_url='login')
def about(request,pk):
    profile = Profile.objects.get(id=pk)
    ctx = {'profile': profile}
    return render(request, 'profiles/about.html',ctx)

@login_required(login_url='login')
def addLike(request,post_id):
    profile = request.user.profile
    post = Post.objects.get(id=post_id)
    try:
        likeexists = Like.objects.filter(post=post,owner=profile).exists()
        if likeexists:
            like = Like.objects.get(post=post,owner=profile)
            like.delete()
        else:
            like = Like.objects.create(post=post,owner=profile,comment=None)
            like.save()
    except:
        pass
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
def addcommentLike(request,comment_id):
    profile = request.user.profile
    comment = Comment.objects.get(id=comment_id)
    try:
        likeexists = Like.objects.filter(comment=comment,owner=profile).exists()
        if likeexists:
            like = Like.objects.get(comment=comment,owner=profile)
            like.delete()
        else:
            like = Like.objects.create(comment=comment,owner=profile)
            like.save()
    except:
        pass
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='login')
def addComment(request,post_id):
    profile = request.user.profile
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(id=post_id)
            comment.owner = profile
            comment.save()
            return redirect('singleprofile', comment.post.owner.id)
    else:
        form = CommentForm()
    return render(request, 'profiles/commentform.html', {'form': form})

@login_required(login_url='login')
def viewComments(request,post_id):
    post = Post.objects.get(id=post_id)
    profile = post.owner
    comments = post.comment_set.all()
    ctx = {'comments':comments,'profile':profile,'post':post}
    return render(request, 'profiles/comments.html',ctx)

@login_required(login_url='login')
def editComment(request,comment_id):
    profile = request.user.profile
    comment = Comment.objects.get(id=comment_id)
    if comment.owner == profile:
        if request.method == 'POST':
            form = CommentForm(request.POST,instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.owner = profile
                comment.save()
                return redirect('viewcomments', comment.post.id)
        else:
            form = CommentForm(instance=comment)
    else:
        return HttpResponse('Oops Something Went Wrong!')
    return render(request, 'profiles/commentform.html',{'form': form})



@login_required(login_url='login')
def editPost(request,post_id):
    profile = request.user.profile
    post = Post.objects.get(id=post_id)
    if post.owner == profile:
        if request.method == 'POST':
            form = PostForm(request.POST,request.FILES,instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.owner = profile
                post.save()
                return redirect('singleprofile', profile.id)
        else:
            form = PostForm(instance=post)
    else:
        return HttpResponse('Oops Something Went Wrong! Go Back and try again!')
    return render(request, 'profiles/postform.html',{'form': form})

@login_required(login_url='login')
def createPost(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = profile
            post.save()
            return redirect('singleprofile', profile.id)
    else:
        form = PostForm()
    return render(request, 'profiles/postform.html',{'form': form})




@login_required(login_url='login')
def deletePost(request,post_id):
    profile = request.user.profile
    post = Post.objects.get(id=post_id, owner=profile)
    post.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='login')
def deleteComment(request,comment_id):
    profile = request.user.profile
    comment = Comment.objects.get(id=comment_id, owner=profile)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



@login_required(login_url='login')
def addPhoto(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = PhotoForm(request.POST,request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = profile
            photo.save()
            return redirect('photos', profile.id)
    else:
        form = PhotoForm()
    return render(request, 'profiles/photoform.html',{'form': form})


@login_required(login_url='login')
def addVideo(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.owner = profile
            video.save()
            return redirect('videos', profile.id)
    else:
        form = VideoForm()
    return render(request, 'profiles/videoform.html',{'form': form})

@login_required(login_url='login')
def viewPhotos(request,pk):
    profile = Profile.objects.get(id=pk)
    photos = profile.photo_set.all()
    ctx = {'photos': photos,'profile': profile}
    return render(request, 'profiles/photos.html',ctx)


@login_required(login_url='login')
def viewVideos(request,pk):
    profile = Profile.objects.get(id=pk)
    videos = profile.video_set.all()
    ctx = {'videos': videos,'profile': profile}
    return render(request, 'profiles/vidoes.html',ctx)

@login_required(login_url='login')
def viewFriends(request,pk):
    profile = Profile.objects.get(id=pk)
    friends = profile.friends.all()
    ctx = {'friends': friends,'profile': profile}
    return render(request, 'profiles/friends.html',ctx)

@login_required(login_url='login')
def addFriends(request,pk):
    profile = Profile.objects.get(id=pk)
    friendrequest = FriendRequests.objects.create(sender=request.user,
        reciever=profile)
    if friendrequest.sender.profile == friendrequest.reciever:
        friendrequest.delete()
        messages.info(request,'you can not add your self as a friend!')
    else:
        friendrequest.save()
    return redirect('singleprofile', profile.id)

@login_required(login_url='login')
def viewFriendRequests(request):
    profile = request.user.profile
    friendrequests = FriendRequests.objects.filter(reciever=profile)
    ctx = {'friendrequests': friendrequests}
    return render(request, 'profiles/friendrequests.html',ctx)

@login_required(login_url='login')
def acceptRequest(request,request_id):
    friendrequest = FriendRequests.objects.get(id=request_id)
    friendrequest.reciever.friends.add(friendrequest.sender.profile)
    friendrequest.sender.profile.friends.add(friendrequest.reciever)
    friendrequest.delete()
    return redirect('friends', request.user.profile.id)


@login_required(login_url='login')
def refuseRequest(request,request_id):
    friendrequest = FriendRequests.objects.get(id=request_id)
    friendrequest.delete()
    return redirect('friendrequests', request.user.profile.id)

@login_required(login_url='login')
def unfriend(request,pk):
    profile = Profile.objects.get(id=pk)
    current_user = request.user
    friends_list = list(current_user.profile.friends.all())
    print(friends_list)
    ids = []
    for i in friends_list:
        ids.append(i.id)
    if profile in friends_list:
        index = friends_list.index(profile)
        profile_id = ids[index]
        current_user.profile.friends.remove(profile_id)
        profile.friends.remove(current_user.profile)
        current_user.profile.save()
        return redirect('friends', current_user.profile.id)


@login_required(login_url='login')
def viewPage(request,page_id):
    current_user = request.user
    page = Page.objects.get(id=page_id)
    posts = page.post_set.all()
    subscribers = list(page.subscribers.all())
    if current_user.profile in subscribers:
        asubscriber = True
    else:
        asubscriber = False
    ctx = {'page': page,'asubscriber':asubscriber,'posts':posts}
    return render(request, 'profiles/page.html', ctx)


@login_required(login_url='login')
def subscriber(request,page_id):
    current_user = request.user
    page = Page.objects.get(id=page_id)
    subscribers = list(page.subscribers.all())
    if current_user.profile in subscribers:
        page.subscribers.remove(current_user.profile)
        current_user.profile.pages.remove(page)
        page.save()
        messages.success(request,'unfollowed!')
    else:
        page.subscribers.add(current_user.profile)
        current_user.profile.pages.add(page)
        page.save()
        messages.success(request,'you now follow this page!')
    return redirect('page', page.id)

@login_required(login_url='login')
def addPagephoto(request,page_id):
    current_user = request.user
    page = Page.objects.get(id=page_id)
    if current_user == page.owner:
        if request.method == "POST":
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.page = page
                photo.save()
                messages.success(request,'photo added!')
                return redrect('pagephotos', page.id)
        else:
            form = PhotoForm()
    else:
        return HttpResponse('Oops Something Went Wrong! Go Back!')
    ctx = {'form': form}
    return render(request, 'profiles/photoform.html', ctx)

@login_required(login_url='login')
def addPagevideo(request,page_id):
    current_user = request.user
    page = Page.objects.get(id=page_id)
    if current_user == page.owner:
        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                video = form.save(commit=False)
                video.page = page
                video.save()
                messages.success(request,'video added!')
                return redirect('pagevideos' ,page.id)
        else:
            form = VideoForm()
    else:
        return HttpResponse('Oops Something Went Wrong! Go Back!')
    ctx = {'form': form}
    return render(request, 'profiles/videoform.html', ctx)

@login_required(login_url='login')
def addPagepost(request,page_id):
    current_user = request.user
    page = Page.objects.get(id=page_id)
    if current_user == page.owner:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.page = page
                post.save()
                messages.success(request,'post added!')
                return redirect('page', page.id)
        else:
            form = PostForm()
    else:
        return HttpResponse('Oops Something Went Wrong! Go Back!')
    ctx = {'form': form}
    return render(request, 'profiles/postform.html', ctx)

@login_required(login_url='login')
def editPagepost(request,post_id):    
    current_user = request.user
    post = Post.objects.get(id=post_id)
    if post.page.owner == current_user:
        post = Post.objects.get(id=post_id)
        if request.method == "POST":
            form = PagePostForm( request.POST,request.FILES,instance=post)
            if form.is_valid():
                post.save()
                messages.success(request,'post updated!')
                return redirect('page', post.page.id)
        else:
            form = PagePostForm(instance=post)
    else:
        return HttpResponse('Oops Soemthing Went Wrong! Go Back!')
    ctx = {'form': form}
    return render(request, 'profiles/postform.html', ctx)


@login_required(login_url='login')
def viewpagePhotos(request,page_id):
    page = Page.objects.get(id=page_id)
    photos = page.photo_set.all()
    ctx = {'photos': photos,'page': page}
    return render(request, 'profiles/pagephotos.html',ctx)


@login_required(login_url='login')
def viewpageVideos(request,page_id):
    page = Page.objects.get(id=page_id)
    videos = page.video_set.all()
    ctx = {'videos': videos,'page': page}
    return render(request, 'profiles/pagevideos.html',ctx)

@login_required(login_url='login')
def viewpageAbout(request,page_id):
    page = Page.objects.get(id=page_id)
    ctx = {'page': page}
    return render(request, 'profiles/pageabout.html',ctx)



@login_required(login_url='login')
def editPage(request, page_id):
    current_user = request.user
    page = Page.objects.get(id=page_id)
    if current_user == page.owner:
        if request.method == "POST":
            form = PageForm(request.POST, request.FILES,instance=page)
            if form.is_valid():
                page = form.save()
                page.owner = current_user
                page.save()
                messages.success(request,'page updated!')
                return redirect('page', page.id)
        else:
            form = PageForm(instance=page)
    else:
        return HttpResponse('Oops! Something went wrong! Go Back and try again!')
    ctx = {
        'form': form,
    }
    return render(request, 'profiles/pageform.html',ctx)


@login_required(login_url='login')
def viewMessages(request):
    profile = request.user.profile
    allmessages = Message.objects.filter(recipient=profile).order_by('-created')
    sentmessages = Message.objects.filter(sender=profile).order_by('-created')
    ctx = {
       'allmessages': allmessages,'sentmessages': sentmessages
    }
    return render(request, 'profiles/messages.html', ctx)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    unreadmessage = Message.objects.get(id=pk)
    if unreadmessage.recipient == profile:
        unreadmessage.is_read = True
        unreadmessage.save()
        ctx = {
        'unreadmessage': unreadmessage,
        }
    elif unreadmessage.sender == unreadmessage.sender:
        ctx = {
        'unreadmessage': unreadmessage,
        }
    else:
        return HttpResponse('Oops Your Are Not Allowed To View This Page!')
    return render(request, 'profiles/message.html', ctx)

@login_required(login_url='login')
def sendAmessage(request,pk):
    sender = request.user.profile
    recipient = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.email = sender.email
            message.name = sender.name
            message.subject =request.POST['subject']
            message.body =request.POST['body']
            message.is_read = False
            message.save()
            messages.success(request,'message sent!')
            return redirect('message',message.id)
    else:
        form = MessageForm()
    ctx = {'form': form}
    return render(request, 'profiles/messageform.html', ctx)
    