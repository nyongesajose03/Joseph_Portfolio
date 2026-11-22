from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.html import escape

from .forms import ContactMessageForm


def home(request):
    form = ContactMessageForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        contact_message = form.save()
        email_sent = EmailMessage(
            subject=f'Portfolio enquiry from {contact_message.name}',
            body=(
                f'Name: {contact_message.name}\n'
                f'Email: {contact_message.email}\n\n'
                f'{contact_message.message}'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[contact_message.email],
        ).send(fail_silently=True)
        if email_sent and 'console' not in settings.EMAIL_BACKEND.lower():
            messages.success(request, 'Thanks for reaching out. Your message has been emailed successfully.')
        elif email_sent:
            messages.info(request, 'Your message was saved successfully. The email notification is currently being printed to the development console.')
        else:
            messages.info(request, 'Your message was saved successfully. Email notifications will be sent once SMTP is configured.')
        return redirect('home')

    return render(request, 'home.html', {'form': form})


def sitemap(request):
    site_url = settings.SITE_URL.rstrip('/') if settings.SITE_URL else request.build_absolute_uri('/').rstrip('/')
    home_url = f'{site_url}{reverse("home")}'
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'<url><loc>{escape(home_url)}</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>'
        '</urlset>'
    )
    return HttpResponse(xml, content_type='application/xml')


def robots(request):
    site_url = settings.SITE_URL.rstrip('/') if settings.SITE_URL else request.build_absolute_uri('/').rstrip('/')
    content = f'User-agent: *\nAllow: /\n\nSitemap: {site_url}/sitemap.xml\n'
    return HttpResponse(content, content_type='text/plain')
