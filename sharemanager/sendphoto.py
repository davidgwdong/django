#from django.contrib.auth.models import User
from sharemanager.models import XPUser
from django.core.mail import EmailMessage
import json
import requests
from django.conf import settings

emailbody = "Hi there: your friend send a secured photo to you, to view the photo, please download xPhoto from @link"


def send_gcm_message(user, data_id):
    """
    Send a GCM message for one or more devices, using json data
    api_key: The API_KEY from your console (https://code.google.com/apis/console, locate Key for Server Apps in
        Google Cloud Messaging for Android)
    regs_id: A list with the devices which will be receiving a message
    data: The dict data which will be send
    collapse_key: A string to group messages, look at the documentation about it:
        http://developer.android.com/google/gcm/gcm.html#request
    """
    print data_id
    print user.gcm_token
    regs_id = list()
    regs_id.append(user.gcm_token)

    message = json.dumps(data_id)
    values = {
        'registration_ids': regs_id,
        'collapse_key': "message" ,
        'data': {"message":str(message)}
    }

    headers = {
        'UserAgent': "GCM-Server",
        'Content-Type': 'application/json',
        'Authorization': 'key=' + settings.GCM_APIKEY,
    }

    response = requests.post(url="https://android.googleapis.com/gcm/send",data=json.dumps(values), headers=headers)

    print response.content
    r = json.loads(response.content)
    return response.content

def sendNotification(instance):
    username = getattr(instance, "shareto")
    print username
    if username:
        if XPUser.objects.filter(username=username).exists():
            send_gcm_message(user = XPUser.objects.get(username=username), data_id = getattr(instance, "id"))
            return

    #user not registered, send email
    email = getattr(instance, "sharetoemail")
    print email
    sendto = [email]
    if email:
        emailsender = EmailMessage('Your friend send a photo to you', emailbody, to=sendto)
        emailsender.send()
