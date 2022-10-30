from django.shortcuts import render ,redirect
from .forms import RegistrationForm, LoginForm
from .models import Account
from django.contrib import messages, auth
from accounts.models import Account 
from django.contrib.auth import authenticate 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = RegistrationForm()
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            phone_number = request.POST['phone_number']
            username = email.split('@')[0]
            user = Account.objects.create(first_name=first_name,
            last_name=last_name,email=email,phone_number=phone_number,username=username)
            user.set_password(password)
            user.save()
            current_site=get_current_site(request)
            mail_subject = "Activate your account to ecommerceready!"
            message = render_to_string("accounts/account_verification.html",
            {
            'user' : user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message ,to=[to_email])
            send_email.send()
            return redirect('/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    ctx = {'form':form}
    return render(request, 'accounts/register.html',ctx)



def login(request):
    if request.user.is_authenticated:
        url = request.META.get('HTTP_REFERER')
        try:
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))
            if 'next' in params:
                nextpage = params['next']
                return redirect(nextpage)
        except:
           return redirect('home')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Welcome '+ user.first_name + '!')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect email or password')
            return redirect('login')
    else:
        form = LoginForm()
    ctx = {'form':form}
    return render(request, 'accounts/login.html', ctx)



def logout(request):
    auth.logout(request)
    return redirect('login')




def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user= Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account Activated Successfully!')
        return redirect('login')
    else:
        messages.error(request,'Link Expired!')
        return redirect('login')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject = "Reset Your Password!"
            message = render_to_string("accounts/forgotpasswordemail.html",
            {
            'user' : user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message ,to=[to_email])
            send_email.send()
            messages.success(request, 'An Email with instructions sent to your emailaddress!')
        else:
            messages.error(request, 'Enter a Valid EmailAdress!')
    return render(request, 'accounts/forgotpassword.html')


def resetPassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetPassword')
    else:
        messages.info(request,'Expired Link!')
        return redirect('login')



def resetPassword(request):
    if request.method == "POST":
        password = request.POST['enterpassword']
        confirm  = request.POST['confirmpassword']

        if password == confirm:
            uid = request.session.get('uid')
            user= Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Success!')
            return redirect('login')
        else:
            messages.info(request, 'Password doesn\'t match!')
            return redirect('resetPassword')

    return render(request, 'accounts/resetPassword.html')




