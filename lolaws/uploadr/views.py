from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.mail import send_mail
from django.conf import settings

from lolaws.uploadr.models import StoredImage
from lolaws.uploadr.forms import StoredImageUploadForm, EmailImageForm

def send_email(subject='', message='', recipient=None):
    """
    sends emails
    """
    if recipient is None:
        return

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    if from_email and subject and message:
        send_mail(subject, message, from_email, [recipient,])


def upload(request, template_name='uploadr/upload.html'):
    """
    handles file uploads
    """
    if request.method == 'POST':
        upload_form = StoredImageUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            image = upload_form.save()
            return redirect('uploadr-success', image_id=image.pk)
    else:
        upload_form = StoredImageUploadForm()

    recent = StoredImage.objects.all()[:10]
    data = {'form':upload_form, 'recent_uploads':recent}
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def success(request, image_id, template_name='uploadr/success.html'):
    """
    success on file upload, lets you email a link to the upload
    """
    upload = get_object_or_404(StoredImage, pk=image_id)
    message = ''
    color = '#fff'  #HARD CODE'N HTML INTO MY VIEW LIKE A BOSS

    if request.method == 'POST':
        email_form = EmailImageForm(request.POST)
        if email_form.is_valid():
            email_address = email_form.cleaned_data['address']

            email_message = 'Someone wants you to see this image: {0}'.format(upload.image.url)
            email_subject = 'YOU GOT A MESSAGE BRO'
            try:
                send_email(email_subject, email_message, email_address)
            except Exception:
                message = 'Email Failed'
                color = '#f00' #lol who needs notifications
            else:
                message = 'Email Sent to {0}'.format(email_address)
                color = '#0f0' #lol who needs notifications

            email_form=EmailImageForm()
    else:
        email_form = EmailImageForm()

    data = {'upload':upload, 'message':message, 'color':color, 'form':email_form}
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def all(request, template_name='uploadr/all.html'):
    filez = StoredImage.objects.all()

    data = {'filez':filez}
    return render_to_response(template_name, data, context_instance=RequestContext(request))
