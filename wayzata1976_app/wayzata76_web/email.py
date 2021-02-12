from django.core.mail import BadHeaderError, send_mail, mail_admins, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect


def send_contact_info_notice(request):
    first_name = request.POST.get('first_name')
    middle_initial = request.POST.get('middle_initial')
    last_name = request.POST.get('last_name')
    


def send_admin_mail(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            mail_admins(subject, message)
        except BadHeaderError:
            return HttpResponse('Invalid header present')
        return HttpResponseRedirect('/email/thanks/')
    else:
        return HttpResponse('Invalid Form Field') # will catch with form....