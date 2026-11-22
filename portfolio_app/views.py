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
        subject = f'New portfolio inquiry from {contact_message.name}'
        body = (
            f'Name: {contact_message.name}\n'
            f'Email: {contact_message.email}\n\n'
            f'Message:\n{contact_message.message}'
        )

        try:
            EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[contact_message.email],
            ).send(fail_silently=False)
        except Exception:
            messages.warning(
                request,
                'Your message was saved, but the email notification could not be sent. '
                'Please email me directly at nyongesajose03@gmail.com.',
            )
        else:
            messages.success(request, 'Thank you! Your message has been sent.')

        return redirect(f'{reverse("home")}#contact')

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
