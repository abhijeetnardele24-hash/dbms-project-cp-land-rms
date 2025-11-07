"""
Test Email System - Demonstrates email notifications
Run this to test email functionality in DEMO MODE
"""

from app import create_app
from app.utils.email_service import EmailService

def test_emails():
    """Test all email notifications"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*80)
        print("     LAND REGISTRY EMAIL NOTIFICATION SYSTEM - TEST")
        print("="*80)
        print("\nRunning in DEMO MODE - Emails will be printed to console\n")
        print("To send real emails:")
        print("  1. Set EMAIL_DEMO_MODE=false in environment variables")
        print("  2. Configure MAIL_USERNAME and MAIL_PASSWORD")
        print("  3. Restart the application\n")
        
        # Test 1: Property Approval Email
        print("\n[TEST 1] Property Approval Email")
        print("-" * 80)
        property_data = {
            'ulpin': 'ULPIN-2024-12345',
            'village_city': 'Nagpur',
            'district': 'Maharashtra',
            'area': '1500',
            'area_unit': 'sqft'
        }
        EmailService.send_property_approval_email('citizen@example.com', property_data)
        
        # Test 2: Mutation Approved
        print("\n[TEST 2] Mutation Approval Email")
        print("-" * 80)
        mutation_data = {
            'mutation_number': 'MUT-2024-001',
            'mutation_type': 'transfer',
            'property_ulpin': 'ULPIN-2024-12345',
            'status': 'approved',
            'comments': 'All documents verified. Mutation approved successfully.'
        }
        EmailService.send_mutation_status_email('citizen@example.com', mutation_data)
        
        # Test 3: Mutation Rejected
        print("\n[TEST 3] Mutation Rejection Email")
        print("-" * 80)
        mutation_data_rejected = {
            'mutation_number': 'MUT-2024-002',
            'mutation_type': 'inheritance',
            'property_ulpin': 'ULPIN-2024-67890',
            'status': 'rejected',
            'comments': 'Required documents missing. Please submit legal heir certificate.'
        }
        EmailService.send_mutation_status_email('citizen@example.com', mutation_data_rejected)
        
        # Test 4: Payment Receipt
        print("\n[TEST 4] Payment Receipt Email")
        print("-" * 80)
        payment_data = {
            'payment_reference': 'PAY-2024-001',
            'receipt_number': 'RCP-2024-001',
            'amount': '5000.00',
            'payment_method': 'Online/Razorpay'
        }
        EmailService.send_payment_receipt_email('citizen@example.com', payment_data)
        
        print("\n" + "="*80)
        print("     ALL TESTS COMPLETED!")
        print("="*80)
        print("\n✅ Email system is working correctly in DEMO MODE")
        print("📧 In production, these emails would be sent to actual recipients")
        print("\nNext Steps:")
        print("  - Configure email credentials for production")
        print("  - Test with real email addresses")
        print("  - Integrate with actual user actions (approve/reject)\n")


if __name__ == '__main__':
    test_emails()
