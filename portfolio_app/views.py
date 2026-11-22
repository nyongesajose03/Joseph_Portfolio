from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import ContactMessageForm


def home(request):
    form = ContactMessageForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        contact_message = form.save()
        EmailMessage(
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
        messages.success(request, 'Thanks for reaching out. Your message has been sent successfully.')
        return redirect('home')

    return render(request, 'home.html', {'form': form})
