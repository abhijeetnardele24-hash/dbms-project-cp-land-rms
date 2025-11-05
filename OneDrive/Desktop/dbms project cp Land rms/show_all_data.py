"""
Display all data from the database table by table
"""

from app import create_app
from app.models import (
    db, User, Property, Owner, Ownership, Mutation, MutationDocument,
    Document, Payment, Notification, AuditLog, TaxAssessment,
    LandCategory, UsageType, DocumentType, PropertyStatus,
    PropertyValuation, PropertyInspection, PropertyDispute, PropertyMortgage,
    Message, Comment, Task, Meeting, Certificate, Complaint
)

app = create_app()

def print_separator(title):
    """Print a formatted separator with title"""
    print('\n' + '='*80)
    print(f' {title}')
    print('='*80)

def show_users():
    print_separator('USERS TABLE')
    users = User.query.all()
    print(f'\nTotal Users: {len(users)}\n')
    
    if users:
        for user in users:
            print(f'ID: {user.id}')
            print(f'  Email: {user.email}')
            print(f'  Full Name: {user.full_name}')
            print(f'  Role: {user.role}')
            print(f'  Phone: {user.phone_number or "N/A"}')
            print(f'  Is Active: {user.is_active}')
            print(f'  Created: {user.created_at}')
            print('-' * 80)
    else:
        print('No users found.')

def show_owners():
    print_separator('OWNERS TABLE')
    owners = Owner.query.all()
    print(f'\nTotal Owners: {len(owners)}\n')
    
    if owners:
        for owner in owners:
            print(f'ID: {owner.id}')
            print(f'  Name: {owner.full_name}')
            print(f'  Father/Guardian: {owner.father_guardian_name or "N/A"}')
            print(f'  Aadhaar: {owner.aadhaar_number or "N/A"}')
            print(f'  PAN: {owner.pan_number or "N/A"}')
            print(f'  Phone: {owner.phone_number or "N/A"}')
            print(f'  Email: {owner.email or "N/A"}')
            print(f'  Address: {owner.address or "N/A"}')
            print('-' * 80)
    else:
        print('No owners found.')

def show_properties():
    print_separator('PROPERTIES TABLE')
    properties = Property.query.all()
    print(f'\nTotal Properties: {len(properties)}\n')
    
    if properties:
        for prop in properties:
            print(f'ID: {prop.id}')
            print(f'  ULPIN: {prop.ulpin or "N/A"}')
            print(f'  Property Type: {prop.property_type}')
            print(f'  Survey Number: {prop.survey_number}')
            print(f'  Village/City: {prop.village_city}')
            print(f'  Taluka: {prop.taluka}')
            print(f'  District: {prop.district}')
            print(f'  State: {prop.state}')
            print(f'  Pin Code: {prop.pin_code}')
            print(f'  Total Area: {prop.total_area_sqft} sqft')
            print(f'  Land Category: {prop.land_category}')
            print(f'  Market Value: ₹{prop.market_value or 0}')
            print(f'  Status: {prop.status}')
            print(f'  Registered: {prop.registration_date}')
            print('-' * 80)
    else:
        print('No properties found.')

def show_ownerships():
    print_separator('OWNERSHIPS TABLE')
    ownerships = Ownership.query.all()
    print(f'\nTotal Ownerships: {len(ownerships)}\n')
    
    if ownerships:
        for ownership in ownerships:
            print(f'ID: {ownership.id}')
            print(f'  Property ID: {ownership.property_id}')
            print(f'  Owner ID: {ownership.owner_id}')
            print(f'  Ownership Share: {ownership.ownership_share}%')
            print(f'  Start Date: {ownership.start_date}')
            print(f'  End Date: {ownership.end_date or "Current"}')
            print(f'  Is Current: {ownership.is_current}')
            print('-' * 80)
    else:
        print('No ownerships found.')

def show_mutations():
    print_separator('MUTATIONS TABLE')
    mutations = Mutation.query.all()
    print(f'\nTotal Mutations: {len(mutations)}\n')
    
    if mutations:
        for mutation in mutations:
            print(f'ID: {mutation.id}')
            print(f'  Mutation Number: {mutation.mutation_number}')
            print(f'  Type: {mutation.mutation_type}')
            print(f'  Property ID: {mutation.property_id}')
            print(f'  Status: {mutation.status}')
            print(f'  Application Date: {mutation.application_date}')
            print(f'  Approval Date: {mutation.approval_date or "Pending"}')
            print(f'  Applied By: User ID {mutation.applied_by}')
            print(f'  Reviewed By: {mutation.reviewed_by or "Not yet"}')
            print(f'  Reason: {mutation.reason or "N/A"}')
            print('-' * 80)
    else:
        print('No mutations found.')

def show_payments():
    print_separator('PAYMENTS TABLE')
    payments = Payment.query.all()
    print(f'\nTotal Payments: {len(payments)}\n')
    
    if payments:
        for payment in payments:
            print(f'ID: {payment.id}')
            print(f'  Transaction Number: {payment.transaction_number}')
            print(f'  Amount: ₹{payment.amount}')
            print(f'  Payment Type: {payment.payment_type}')
            print(f'  Status: {payment.status}')
            print(f'  Method: {payment.payment_method}')
            print(f'  Property ID: {payment.property_id or "N/A"}')
            print(f'  Paid By: User ID {payment.paid_by}')
            print(f'  Payment Date: {payment.payment_date}')
            print('-' * 80)
    else:
        print('No payments found.')

def show_notifications():
    print_separator('NOTIFICATIONS TABLE')
    notifications = Notification.query.all()
    print(f'\nTotal Notifications: {len(notifications)}\n')
    
    if notifications:
        for notif in notifications:
            print(f'ID: {notif.id}')
            print(f'  User ID: {notif.user_id}')
            print(f'  Title: {notif.title}')
            print(f'  Message: {notif.message}')
            print(f'  Type: {notif.notification_type}')
            print(f'  Is Read: {notif.is_read}')
            print(f'  Created: {notif.created_at}')
            print('-' * 80)
    else:
        print('No notifications found.')

def show_documents():
    print_separator('DOCUMENTS TABLE')
    documents = Document.query.all()
    print(f'\nTotal Documents: {len(documents)}\n')
    
    if documents:
        for doc in documents:
            print(f'ID: {doc.id}')
            print(f'  Document Type: {doc.document_type}')
            print(f'  File Name: {doc.file_name}')
            print(f'  File Path: {doc.file_path}')
            print(f'  Property ID: {doc.property_id or "N/A"}')
            print(f'  Uploaded By: User ID {doc.uploaded_by}')
            print(f'  Upload Date: {doc.upload_date}')
            print('-' * 80)
    else:
        print('No documents found.')

def show_tax_assessments():
    print_separator('TAX ASSESSMENTS TABLE')
    assessments = TaxAssessment.query.all()
    print(f'\nTotal Tax Assessments: {len(assessments)}\n')
    
    if assessments:
        for tax in assessments:
            print(f'ID: {tax.id}')
            print(f'  Property ID: {tax.property_id}')
            print(f'  Assessment Year: {tax.assessment_year}')
            print(f'  Tax Amount: ₹{tax.tax_amount}')
            print(f'  Status: {tax.payment_status}')
            print(f'  Due Date: {tax.due_date}')
            print(f'  Payment Date: {tax.payment_date or "Not paid"}')
            print('-' * 80)
    else:
        print('No tax assessments found.')

def show_audit_logs():
    print_separator('AUDIT LOGS TABLE')
    logs = AuditLog.query.order_by(AuditLog.id.desc()).limit(50).all()
    print(f'\nShowing latest 50 Audit Logs (Total: {AuditLog.query.count()})\n')
    
    if logs:
        for log in logs:
            print(f'ID: {log.id}')
            print(f'  User ID: {log.user_id or "System"}')
            print(f'  Action: {log.action}')
            print(f'  Table: {log.table_name}')
            print(f'  Record ID: {log.record_id}')
            print(f'  Timestamp: {log.timestamp}')
            print(f'  IP Address: {log.ip_address or "N/A"}')
            print('-' * 80)
    else:
        print('No audit logs found.')

def show_master_data():
    print_separator('MASTER DATA TABLES')
    
    print('\n--- Land Categories ---')
    categories = LandCategory.query.all()
    for cat in categories:
        print(f'  {cat.id}. {cat.name} - {cat.description}')
    
    print('\n--- Usage Types ---')
    usages = UsageType.query.all()
    for usage in usages:
        print(f'  {usage.id}. {usage.name} - {usage.description}')
    
    print('\n--- Document Types ---')
    doc_types = DocumentType.query.all()
    for dt in doc_types:
        print(f'  {dt.id}. {dt.name} - Required: {dt.is_required}')
    
    print('\n--- Property Statuses ---')
    statuses = PropertyStatus.query.all()
    for status in statuses:
        print(f'  {status.id}. {status.name} - {status.description}')

def show_advanced_features():
    print_separator('ADVANCED FEATURES DATA')
    
    # Property Valuations
    print('\n--- Property Valuations ---')
    valuations = PropertyValuation.query.all()
    print(f'Total: {len(valuations)}')
    for val in valuations[:10]:  # Show first 10
        print(f'  Property {val.property_id}: ₹{val.valuation_amount} - {val.valuation_date}')
    
    # Property Inspections
    print('\n--- Property Inspections ---')
    inspections = PropertyInspection.query.all()
    print(f'Total: {len(inspections)}')
    for insp in inspections[:10]:
        print(f'  Property {insp.property_id}: {insp.inspection_type} - {insp.inspection_date}')
    
    # Property Disputes
    print('\n--- Property Disputes ---')
    disputes = PropertyDispute.query.all()
    print(f'Total: {len(disputes)}')
    for disp in disputes[:10]:
        print(f'  Property {disp.property_id}: {disp.dispute_type} - Status: {disp.status}')
    
    # Property Mortgages
    print('\n--- Property Mortgages ---')
    mortgages = PropertyMortgage.query.all()
    print(f'Total: {len(mortgages)}')
    for mort in mortgages[:10]:
        print(f'  Property {mort.property_id}: ₹{mort.loan_amount} - {mort.lender_name}')
    
    # Messages
    print('\n--- Messages ---')
    messages = Message.query.all()
    print(f'Total: {len(messages)}')
    
    # Comments
    print('\n--- Comments ---')
    comments = Comment.query.all()
    print(f'Total: {len(comments)}')
    
    # Tasks
    print('\n--- Tasks ---')
    tasks = Task.query.all()
    print(f'Total: {len(tasks)}')
    for task in tasks[:10]:
        print(f'  {task.title}: {task.status} - Due: {task.due_date}')
    
    # Meetings
    print('\n--- Meetings ---')
    meetings = Meeting.query.all()
    print(f'Total: {len(meetings)}')
    
    # Certificates
    print('\n--- Certificates ---')
    certificates = Certificate.query.all()
    print(f'Total: {len(certificates)}')
    
    # Complaints
    print('\n--- Complaints ---')
    complaints = Complaint.query.all()
    print(f'Total: {len(complaints)}')

def main():
    with app.app_context():
        print('\n')
        print('*' * 80)
        print(' LAND REGISTRY MANAGEMENT SYSTEM - COMPLETE DATABASE DUMP')
        print('*' * 80)
        
        # Show all tables one by one
        show_users()
        input('\nPress Enter to continue to OWNERS...')
        
        show_owners()
        input('\nPress Enter to continue to PROPERTIES...')
        
        show_properties()
        input('\nPress Enter to continue to OWNERSHIPS...')
        
        show_ownerships()
        input('\nPress Enter to continue to MUTATIONS...')
        
        show_mutations()
        input('\nPress Enter to continue to PAYMENTS...')
        
        show_payments()
        input('\nPress Enter to continue to NOTIFICATIONS...')
        
        show_notifications()
        input('\nPress Enter to continue to DOCUMENTS...')
        
        show_documents()
        input('\nPress Enter to continue to TAX ASSESSMENTS...')
        
        show_tax_assessments()
        input('\nPress Enter to continue to AUDIT LOGS...')
        
        show_audit_logs()
        input('\nPress Enter to continue to MASTER DATA...')
        
        show_master_data()
        input('\nPress Enter to continue to ADVANCED FEATURES...')
        
        show_advanced_features()
        
        print_separator('END OF DATA DUMP')
        print('\nAll data has been displayed!')

if __name__ == '__main__':
    main()
