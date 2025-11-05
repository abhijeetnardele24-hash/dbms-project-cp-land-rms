"""
Notification utility functions for creating and managing notifications.
"""

from app.models import db
from app.models.notification import Notification
from app.utils.email_utils import send_notification_email


def create_notification(user_id, title, message, notification_type='info', 
                       related_entity_type=None, related_entity_id=None, 
                       priority='normal', send_email=False):
    """
    Create a new notification for a user.
    
    Args:
        user_id: ID of the user to notify
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        related_entity_type: Type of related entity (property, mutation, payment)
        related_entity_id: ID of related entity
        priority: Notification priority (low, normal, high)
        send_email: Whether to also send an email notification
    
    Returns:
        Notification: Created notification object
    """
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        related_entity_type=related_entity_type,
        related_entity_id=related_entity_id,
        priority=priority
    )
    
    db.session.add(notification)
    db.session.commit()
    
    # Send email notification if requested
    if send_email:
        from app.models.user import User
        user = User.query.get(user_id)
        if user and user.email:
            try:
                send_notification_email(user, notification_type, 
                                       title=title, message=message)
                notification.email_sent = True
                notification.email_sent_at = db.func.now()
                db.session.commit()
            except Exception as e:
                # Log error but don't fail the notification creation
                pass
    
    return notification


def send_system_notification(user_ids, title, message, notification_type='system_announcement',
                            priority='normal', send_email=False):
    """
    Send notification to multiple users (e.g., system announcements).
    
    Args:
        user_ids: List of user IDs to notify
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        priority: Notification priority
        send_email: Whether to also send email notifications
    """
    for user_id in user_ids:
        create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            send_email=send_email
        )


def notify_property_status_change(property_id, new_status, user_id):
    """
    Send notification when property status changes.
    
    Args:
        property_id: Property ID
        new_status: New status of the property
        user_id: User to notify (property owner)
    """
    from app.models.property import Property
    property_obj = Property.query.get(property_id)
    
    status_messages = {
        'approved': ('Property Registration Approved', 
                    f'Your property registration for {property_obj.ulpin} has been approved.',
                    'property_approved'),
        'rejected': ('Property Registration Rejected',
                    f'Your property registration has been rejected. Please check the details.',
                    'property_rejected'),
        'under_review': ('Property Under Review',
                        f'Your property registration is now under review.',
                        'info'),
        'documents_verified': ('Documents Verified',
                             f'Your property documents have been verified.',
                             'success')
    }
    
    if new_status in status_messages:
        title, message, notif_type = status_messages[new_status]
        create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notif_type,
            related_entity_type='property',
            related_entity_id=property_id,
            send_email=True
        )


def notify_mutation_status_change(mutation_id, new_status, user_id):
    """
    Send notification when mutation status changes.
    
    Args:
        mutation_id: Mutation ID
        new_status: New status of the mutation
        user_id: User to notify (requester)
    """
    from app.models.mutation import Mutation
    mutation = Mutation.query.get(mutation_id)
    
    status_messages = {
        'approved': ('Mutation Request Approved',
                    f'Your mutation request {mutation.mutation_number} has been approved.',
                    'mutation_approved'),
        'rejected': ('Mutation Request Rejected',
                    f'Your mutation request {mutation.mutation_number} has been rejected.',
                    'mutation_rejected'),
        'under_review': ('Mutation Under Review',
                        f'Your mutation request is now under review.',
                        'info'),
        'information_required': ('Additional Information Required',
                                f'Please provide additional information for your mutation request.',
                                'document_required')
    }
    
    if new_status in status_messages:
        title, message, notif_type = status_messages[new_status]
        create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notif_type,
            related_entity_type='mutation',
            related_entity_id=mutation_id,
            send_email=True
        )


def notify_payment_received(payment_id, user_id):
    """
    Send notification when payment is received.
    
    Args:
        payment_id: Payment ID
        user_id: User to notify
    """
    from app.models.payment import Payment
    payment = Payment.query.get(payment_id)
    
    create_notification(
        user_id=user_id,
        title='Payment Received',
        message=f'Your payment of ₹{payment.amount} has been received successfully. Receipt: {payment.receipt_number}',
        notification_type='payment_confirmed',
        related_entity_type='payment',
        related_entity_id=payment_id,
        send_email=True
    )
