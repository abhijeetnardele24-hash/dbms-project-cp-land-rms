"""
Display current database statistics and sample data
"""

from app import create_app
from app.models import db, User, Property, Mutation, Payment, Owner, Ownership, Notification

app = create_app()

with app.app_context():
    print('='*70)
    print('DATABASE CURRENT STATE')
    print('='*70)
    
    # Users statistics
    total_users = User.query.count()
    admin_count = User.query.filter_by(role='admin').count()
    registrar_count = User.query.filter_by(role='registrar').count()
    officer_count = User.query.filter_by(role='officer').count()
    citizen_count = User.query.filter_by(role='citizen').count()
    
    print(f'\nTotal Users: {total_users}')
    print(f'  - Admins: {admin_count}')
    print(f'  - Registrars: {registrar_count}')
    print(f'  - Officers: {officer_count}')
    print(f'  - Citizens: {citizen_count}')
    
    # Other entities
    print(f'\nTotal Owners: {Owner.query.count()}')
    print(f'Total Properties: {Property.query.count()}')
    print(f'Total Ownerships: {Ownership.query.count()}')
    
    # Mutations statistics
    total_mutations = Mutation.query.count()
    pending_mutations = Mutation.query.filter_by(status='pending').count()
    under_review = Mutation.query.filter_by(status='under_review').count()
    approved = Mutation.query.filter_by(status='approved').count()
    rejected = Mutation.query.filter_by(status='rejected').count()
    
    print(f'\nTotal Mutations: {total_mutations}')
    print(f'  - Pending: {pending_mutations}')
    print(f'  - Under Review: {under_review}')
    print(f'  - Approved: {approved}')
    print(f'  - Rejected: {rejected}')
    
    # Payments statistics
    total_payments = Payment.query.count()
    completed_payments = Payment.query.filter_by(status='completed').count()
    pending_payments = Payment.query.filter_by(status='pending').count()
    
    print(f'\nTotal Payments: {total_payments}')
    print(f'  - Completed: {completed_payments}')
    print(f'  - Pending: {pending_payments}')
    
    print(f'\nTotal Notifications: {Notification.query.count()}')
    
    # Sample data
    print('\n' + '='*70)
    print('SAMPLE DATA')
    print('='*70)
    
    # Sample users
    users = User.query.order_by(User.id).limit(10).all()
    print('\nFirst 10 Users:')
    for u in users:
        print(f'  {u.id:3d}. {u.email:40s} ({u.role:10s}) - {u.full_name}')
    
    # Sample properties
    props = Property.query.order_by(Property.id).limit(10).all()
    print('\nFirst 10 Properties:')
    for p in props:
        ulpin = p.ulpin or 'N/A'
        prop_type = p.property_type or 'N/A'
        village = p.village_city or 'N/A'
        print(f'  {p.id:3d}. {ulpin:20s} - {prop_type:15s} in {village}')
    
    # Sample mutations
    muts = Mutation.query.order_by(Mutation.id).limit(10).all()
    print('\nFirst 10 Mutations:')
    for m in muts:
        print(f'  {m.id:3d}. {m.mutation_number:15s} - {m.mutation_type:12s} ({m.status})')
    
    # Property type distribution
    print('\n' + '='*70)
    print('PROPERTY TYPE DISTRIBUTION')
    print('='*70)
    from sqlalchemy import func
    prop_types = db.session.query(
        Property.property_type,
        func.count(Property.id).label('count')
    ).group_by(Property.property_type).all()
    
    for pt, count in prop_types:
        print(f'  {pt:15s}: {count} properties')
    
    # Mutation type distribution
    print('\n' + '='*70)
    print('MUTATION TYPE DISTRIBUTION')
    print('='*70)
    mut_types = db.session.query(
        Mutation.mutation_type,
        func.count(Mutation.id).label('count')
    ).group_by(Mutation.mutation_type).all()
    
    for mt, count in mut_types:
        print(f'  {mt:15s}: {count} requests')
    
    print('\n' + '='*70)
    print('SUMMARY')
    print('='*70)
    print(f'\nYour database now contains:')
    print(f'  - {total_users} users across all roles')
    print(f'  - {Property.query.count()} properties with complete details')
    print(f'  - {total_mutations} mutation requests ({pending_mutations} pending for officer review)')
    print(f'  - {total_payments} payment records')
    print(f'\nAll passwords are: 1234')
    print(f'\nThe database is ready for recruiter demonstrations!')
    print('='*70)
