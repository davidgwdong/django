from django.contrib.auth.models import User
from django.core.mail import EmailMessage

emailbody = "Hi there: your friend send a secured photo to you, to view the photo, please download xPhoto from @link"

def pushNotification():
    print "push notification to: " + username

def sendNotification(request):
    data = request.data
    print data
    username = data["shareto"]
    print username
    if username:
        if User.objects.filter(username=username).exists():
            pushNotification()
            return

    #user not registered, send email
    email = data["sharetoemail"]
    print email
    sendto = [email]
    if email:
        emailsender = EmailMessage('Your friend send a photo to you', emailbody, to=sendto)
        emailsender.send()
