"""
Email utility functions for sending email notifications.
"""

from flask import current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread


def send_async_email(app, msg):
    """
    Send email asynchronously to avoid blocking the main thread.
    """
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            app.logger.error(f'Failed to send email: {str(e)}')


def send_email(subject, recipients, text_body=None, html_body=None, sender=None):
    """
    Send an email.
    
    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        text_body: Plain text body
        html_body: HTML body
        sender: Sender email (optional, uses default from config)
    """
    if not sender:
        sender = current_app.config['MAIL_DEFAULT_SENDER']
    
    msg = Message(subject, recipients=recipients, sender=sender)
    
    if text_body:
        msg.body = text_body
    if html_body:
        msg.html = html_body
    
    # Send asynchronously
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_notification_email(user, notification_type, **kwargs):
    """
    Send notification email based on type.
    
    Args:
        user: User object
        notification_type: Type of notification (property_approved, mutation_approved, etc.)
        **kwargs: Additional context for email template
    """
    email_templates = {
        'property_approved': {
            'subject': 'Property Registration Approved',
            'template': 'emails/property_approved.html'
        },
        'property_rejected': {
            'subject': 'Property Registration Rejected',
            'template': 'emails/property_rejected.html'
        },
        'mutation_approved': {
            'subject': 'Mutation Request Approved',
            'template': 'emails/mutation_approved.html'
        },
        'mutation_rejected': {
            'subject': 'Mutation Request Rejected',
            'template': 'emails/mutation_rejected.html'
        },
        'payment_confirmed': {
            'subject': 'Payment Confirmation',
            'template': 'emails/payment_confirmed.html'
        },
        'document_required': {
            'subject': 'Additional Documents Required',
            'template': 'emails/document_required.html'
        }
    }
    
    if notification_type not in email_templates:
        current_app.logger.warning(f'Unknown notification type: {notification_type}')
        return
    
    template_info = email_templates[notification_type]
    
    # Add user to context
    kwargs['user'] = user
    kwargs['app_name'] = current_app.config.get('APP_NAME', 'LRMS')
    
    try:
        html_body = render_template(template_info['template'], **kwargs)
        send_email(
            subject=template_info['subject'],
            recipients=[user.email],
            html_body=html_body
        )
    except Exception as e:
        current_app.logger.error(f'Failed to send notification email: {str(e)}')
