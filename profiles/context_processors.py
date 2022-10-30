from accounts.models import FriendRequests , Profile 
from profiles.models import Message

def friendrequestsCount(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        friendrequests = FriendRequests.objects.filter(reciever=profile)
    else:
        friendrequests = FriendRequests.objects.none()
    return dict(friendrequests=friendrequests)


def messagesCount(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        unreadmessages = Message.objects.filter(recipient=profile,is_read=False)
    else:
        unreadmessages = Message.objects.none()
    return dict(unreadmessages=unreadmessages)