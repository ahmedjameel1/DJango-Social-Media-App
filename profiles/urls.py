from django.urls import path
from . import views

urlpatterns = [
    path('singleprofile/<str:pk>/', views.singleprofile, name='singleprofile'),
    path('editprofile/', views.editProfile, name='editProfile'),
    path('about/<str:pk>/', views.about, name='about'),
    path('addlike/<int:post_id>/', views.addLike, name='addLike'),
    path('addcomment/<int:post_id>/', views.addComment, name='addComment'),
    path('viewcomments/<int:post_id>/', views.viewComments, name='viewcomments'),
    path('addcommentLike/<int:comment_id>/', views.addcommentLike, name='addcommentLike'),
    path('editpost/<int:post_id>/', views.editPost, name='editPost'),
    path('createpost/', views.createPost, name='createpost'),
    path('editcomment/<int:comment_id>/', views.editComment, name='editComment'),
    path('deletepost/<int:post_id>/', views.deletePost, name='deletePost'),
    path('deletecomment/<int:comment_id>/', views.deleteComment, name='deleteComment'),
    path('addphoto/', views.addPhoto, name='addphoto'),
    path('addvideo/', views.addVideo, name='addvideo'),
    path('viewphotos/<str:pk>/', views.viewPhotos, name='photos'),
    path('viewvideos/<str:pk>/', views.viewVideos, name='videos'),
    path('viewfriends/<str:pk>/', views.viewFriends, name='friends'),
    path('addfriend/<str:pk>/', views.addFriends, name='addfriend'),
    path('frindrequests/', views.viewFriendRequests, name='friendrequests'),
    path('acceptrequest/<int:request_id>/', views.acceptRequest, name='acceptrequest'),
    path('refuserequests/<int:request_id>/', views.refuseRequest, name='refuserequest'),
    path('unfriend/<str:pk>/', views.unfriend, name='unfriend'),
    path('viewspage/<int:page_id>/', views.viewPage, name='page'),
    path('viewpagephotos/<int:page_id>/', views.viewpagePhotos, name='pagephotos'),
    path('viewpagevideos/<int:page_id>/', views.viewpageVideos, name='pagevideos'),
    path('viewpageabout/<int:page_id>/', views.viewpageAbout, name='aboutpage'),
    path('subscribeorun/<int:page_id>/', views.subscriber, name='subscribe'),
    path('addpagephoto/<int:page_id>/', views.addPagephoto, name='addpagephoto'),
    path('addpagevideo/<int:page_id>/', views.addPagevideo, name='addpagevideo'),
    path('addpagepost/<int:page_id>/', views.addPagepost, name='addpagepost'),
    path('editpagepost/<int:post_id>/', views.editPagepost, name='editpagepost'),
    path('editpage/<int:page_id>/', views.editPage, name='editPage'),
    path('viewmessages/', views.viewMessages, name='messages'),
    path('viewmessage/<str:pk>/', views.viewMessage, name='message'),
    path('sendmessage/<str:pk>/', views.sendAmessage, name='sendmessage'),










]