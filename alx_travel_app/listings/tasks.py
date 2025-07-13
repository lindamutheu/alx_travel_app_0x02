#!/usr/bin/env python3
"""Celery tasks for listings app"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(user_email, booking_id):
    """
    Send booking confirmation email asynchronously
    """
    subject = 'Booking Confirmation'
    message = f"Thank you for your booking! Your booking ID is {booking_id}."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

