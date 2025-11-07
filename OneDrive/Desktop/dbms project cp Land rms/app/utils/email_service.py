"""
Enhanced Email Notification Service
Sends professional emails for property approvals, mutations, and payments
"""

from flask import current_app, render_template_string
from flask_mail import Message
from app import mail
from datetime import datetime
import os

# Demo Mode: Set to True to print emails to console instead of sending
# Set to False when email credentials are configured
DEMO_MODE = os.environ.get('EMAIL_DEMO_MODE', 'true').lower() == 'true'


class EmailService:
    """Professional email notification service"""
    
    @staticmethod
    def send_property_approval_email(user_email, property_data):
        """Send email when property is approved"""
        if DEMO_MODE:
            print("\n" + "="*70)
            print("📧 [DEMO MODE] Property Approval Email")
            print("="*70)
            print(f"TO: {user_email}")
            print(f"SUBJECT: 🎉 Property Approved - {property_data.get('ulpin', 'N/A')}")
            print(f"Property ULPIN: {property_data.get('ulpin', 'N/A')}")
            print(f"Location: {property_data.get('village_city', 'N/A')}, {property_data.get('district', 'N/A')}")
            print(f"Area: {property_data.get('area', 'N/A')} {property_data.get('area_unit', 'sqft')}")
            print(f"Status: ✅ Email would be sent in production")
            print("="*70 + "\n")
            return True
        
        try:
            subject = f"🎉 Property Approved - {property_data.get('ulpin', 'N/A')}"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .property-details {{ background: #f0f4f8; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                    .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Property Approved!</h1>
                        <p>Your property registration has been successfully approved</p>
                    </div>
                    <div class="content">
                        <p>Dear Property Owner,</p>
                        <p>We are pleased to inform you that your property registration has been <strong>approved</strong> by our Land Registry Department.</p>
                        
                        <div class="property-details">
                            <h3>Property Details:</h3>
                            <p><strong>ULPIN:</strong> {property_data.get('ulpin', 'N/A')}</p>
                            <p><strong>Location:</strong> {property_data.get('village_city', 'N/A')}, {property_data.get('district', 'N/A')}</p>
                            <p><strong>Area:</strong> {property_data.get('area', 'N/A')} {property_data.get('area_unit', 'sqft')}</p>
                            <p><strong>Approval Date:</strong> {datetime.now().strftime('%d %B %Y')}</p>
                        </div>
                        
                        <p>You can now:</p>
                        <ul>
                            <li>View your property certificate online</li>
                            <li>Download PDF certificate</li>
                            <li>Submit mutation requests</li>
                            <li>Make tax payments</li>
                        </ul>
                        
                        <a href="http://localhost:5000/citizen/my-properties" class="button">View My Properties</a>
                        
                        <p style="margin-top: 30px;">Thank you for registering your property with us.</p>
                        <p>Best regards,<br><strong>Land Registry Management System</strong></p>
                    </div>
                    <div class="footer">
                        <p>This is an automated email. Please do not reply.</p>
                        <p>&copy; 2025 Land Registry Management System. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(subject=subject,
                         recipients=[user_email],
                         html=html_body)
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending property approval email: {str(e)}")
            return False
    
    @staticmethod
    def send_mutation_status_email(user_email, mutation_data):
        """Send email when mutation status changes"""
        status = mutation_data.get('status', 'updated')
        emoji = "✅" if status == "approved" else "⏳" if status == "pending" else "❌"
        
        if DEMO_MODE:
            print("\n" + "="*70)
            print(f"📧 [DEMO MODE] Mutation Status Email")
            print("="*70)
            print(f"TO: {user_email}")
            print(f"SUBJECT: {emoji} Mutation {status.title()} - {mutation_data.get('mutation_number', 'N/A')}")
            print(f"Mutation Number: {mutation_data.get('mutation_number', 'N/A')}")
            print(f"Type: {mutation_data.get('mutation_type', 'N/A').title()}")
            print(f"Property: {mutation_data.get('property_ulpin', 'N/A')}")
            print(f"Status: {status.upper()}")
            if mutation_data.get('comments'):
                print(f"Comments: {mutation_data.get('comments')}")
            print(f"Status: ✅ Email would be sent in production")
            print("="*70 + "\n")
            return True
        
        try:
            
            subject = f"{emoji} Mutation {status.title()} - {mutation_data.get('mutation_number', 'N/A')}"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; }}
                    .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .mutation-details {{ background: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ff9800; }}
                    .status {{ display: inline-block; padding: 8px 20px; border-radius: 20px; font-weight: bold; margin: 10px 0; }}
                    .status-approved {{ background: #4caf50; color: white; }}
                    .status-pending {{ background: #ffc107; color: white; }}
                    .status-rejected {{ background: #f44336; color: white; }}
                    .button {{ display: inline-block; padding: 12px 30px; background: #f5576c; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>{emoji} Mutation Status Update</h1>
                        <p>Your mutation request has been {status}</p>
                    </div>
                    <div class="content">
                        <p>Dear User,</p>
                        <p>Your mutation request status has been updated.</p>
                        
                        <div class="mutation-details">
                            <h3>Mutation Details:</h3>
                            <p><strong>Mutation Number:</strong> {mutation_data.get('mutation_number', 'N/A')}</p>
                            <p><strong>Type:</strong> {mutation_data.get('mutation_type', 'N/A').title()}</p>
                            <p><strong>Property:</strong> {mutation_data.get('property_ulpin', 'N/A')}</p>
                            <p><strong>Status:</strong> <span class="status status-{status}">{status.upper()}</span></p>
                            <p><strong>Updated On:</strong> {datetime.now().strftime('%d %B %Y, %I:%M %p')}</p>
                        </div>
                        
                        {f'<p><strong>Officer Comments:</strong> {mutation_data.get("comments", "No comments")}</p>' if mutation_data.get('comments') else ''}
                        
                        <a href="http://localhost:5000/citizen/my-mutations" class="button">View Mutation Details</a>
                        
                        <p style="margin-top: 30px;">Thank you for using our services.</p>
                        <p>Best regards,<br><strong>Land Registry Management System</strong></p>
                    </div>
                    <div class="footer">
                        <p>This is an automated email. Please do not reply.</p>
                        <p>&copy; 2025 Land Registry Management System. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(subject=subject,
                         recipients=[user_email],
                         html=html_body)
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending mutation status email: {str(e)}")
            return False
    
    @staticmethod
    def send_payment_receipt_email(user_email, payment_data):
        """Send payment receipt via email"""
        if DEMO_MODE:
            print("\n" + "="*70)
            print("📧 [DEMO MODE] Payment Receipt Email")
            print("="*70)
            print(f"TO: {user_email}")
            print(f"SUBJECT: 💳 Payment Receipt - {payment_data.get('payment_reference', 'N/A')}")
            print(f"Receipt Number: {payment_data.get('receipt_number', 'N/A')}")
            print(f"Amount: ₹ {payment_data.get('amount', '0.00')}")
            print(f"Payment Method: {payment_data.get('payment_method', 'N/A')}")
            print(f"Status: ✅ Email would be sent in production")
            print("="*70 + "\n")
            return True
        
        try:
            subject = f"💳 Payment Receipt - {payment_data.get('payment_reference', 'N/A')}"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; }}
                    .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .receipt {{ background: #e8f5e9; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px dashed #4caf50; }}
                    .amount {{ font-size: 32px; color: #4caf50; font-weight: bold; text-align: center; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                    table {{ width: 100%; border-collapse: collapse; }}
                    td {{ padding: 8px; border-bottom: 1px solid #eee; }}
                    td:first-child {{ font-weight: bold; width: 40%; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>💳 Payment Successful!</h1>
                        <p>Your payment has been received</p>
                    </div>
                    <div class="content">
                        <p>Dear Customer,</p>
                        <p>Thank you for your payment. Your transaction has been processed successfully.</p>
                        
                        <div class="receipt">
                            <h3 style="text-align: center; color: #4caf50; margin-top: 0;">PAYMENT RECEIPT</h3>
                            <div class="amount">₹ {payment_data.get('amount', '0.00')}</div>
                            
                            <table>
                                <tr>
                                    <td>Receipt Number:</td>
                                    <td>{payment_data.get('receipt_number', 'N/A')}</td>
                                </tr>
                                <tr>
                                    <td>Payment Reference:</td>
                                    <td>{payment_data.get('payment_reference', 'N/A')}</td>
                                </tr>
                                <tr>
                                    <td>Transaction ID:</td>
                                    <td>{payment_data.get('transaction_id', 'N/A')}</td>
                                </tr>
                                <tr>
                                    <td>Payment Type:</td>
                                    <td>{payment_data.get('payment_type', 'N/A').title()}</td>
                                </tr>
                                <tr>
                                    <td>Payment Method:</td>
                                    <td>{payment_data.get('payment_method', 'N/A').title()}</td>
                                </tr>
                                <tr>
                                    <td>Date & Time:</td>
                                    <td>{datetime.now().strftime('%d %B %Y, %I:%M %p')}</td>
                                </tr>
                                <tr>
                                    <td>Status:</td>
                                    <td style="color: #4caf50; font-weight: bold;">✓ COMPLETED</td>
                                </tr>
                            </table>
                        </div>
                        
                        <p style="text-align: center; color: #666; font-size: 14px;">
                            Please keep this receipt for your records.<br>
                            You can download the PDF version from your dashboard.
                        </p>
                        
                        <p style="margin-top: 30px;">Thank you for your payment.</p>
                        <p>Best regards,<br><strong>Land Registry Management System</strong></p>
                    </div>
                    <div class="footer">
                        <p>This is an automated email. Please do not reply.</p>
                        <p>&copy; 2025 Land Registry Management System. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(subject=subject,
                         recipients=[user_email],
                         html=html_body)
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending payment receipt email: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(user_email, user_name):
        """Send welcome email to new users"""
        try:
            subject = "🎊 Welcome to Land Registry Management System"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .features {{ background: #f0f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎊 Welcome!</h1>
                        <p>Your account has been created successfully</p>
                    </div>
                    <div class="content">
                        <p>Dear {user_name},</p>
                        <p>Welcome to the <strong>Land Registry Management System</strong>! We're excited to have you on board.</p>
                        
                        <div class="features">
                            <h3>What you can do:</h3>
                            <ul>
                                <li>✅ Register new properties</li>
                                <li>✅ Submit mutation requests</li>
                                <li>✅ Make tax payments online</li>
                                <li>✅ Download certificates</li>
                                <li>✅ Track your applications</li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="http://localhost:5000/auth/login" class="button">Login to Dashboard</a>
                        </div>
                        
                        <p>If you have any questions or need assistance, please don't hesitate to contact us.</p>
                        <p>Best regards,<br><strong>Land Registry Management System Team</strong></p>
                    </div>
                    <div class="footer">
                        <p>This is an automated email. Please do not reply.</p>
                        <p>&copy; 2025 Land Registry Management System. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(subject=subject,
                         recipients=[user_email],
                         html=html_body)
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending welcome email: {str(e)}")
            return False


# Convenience functions
def send_property_approved(user_email, property_data):
    return EmailService.send_property_approval_email(user_email, property_data)

def send_mutation_update(user_email, mutation_data):
    return EmailService.send_mutation_status_email(user_email, mutation_data)

def send_payment_receipt(user_email, payment_data):
    return EmailService.send_payment_receipt_email(user_email, payment_data)

def send_welcome(user_email, user_name):
    return EmailService.send_welcome_email(user_email, user_name)
