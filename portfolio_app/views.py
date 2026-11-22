from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.html import escape

from .forms import ContactMessageForm


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Portfolio Inquiry from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                'nyongesajose03@gmail.com',  # From email
                ['nyongesajose03@gmail.com'],  # To email (your inbox)
                fail_silently=False,
            )
            messages.success(request, "Thank you! Your message has been sent.")
        except Exception:
            messages.error(request, "Something went wrong. Please email me directly at nyongesajose03@gmail.com.")

        return redirect('/#contact')
    return render(request, 'home.html')


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
