"""
Script to add more users to the database to reach 17 total users.
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)

from app import create_app
from app.models import db, User

app = create_app()

def add_users():
    with app.app_context():
        # Count existing users
        existing_count = User.query.count()
        print(f"Current user count: {existing_count}")
        
        target_count = 17
        users_to_add = target_count - existing_count
        
        if users_to_add <= 0:
            print(f"Already have {existing_count} users. No need to add more.")
            return
        
        print(f"Adding {users_to_add} users to reach {target_count} total...")
        
        # Indian names for realistic data
        indian_names = [
            "Priya Sharma", "Rahul Verma", "Deepak Gupta", "Pooja Singh",
            "Arjun Patel", "Neha Kumar", "Sanjay Reddy", "Anjali Yadav",
            "Manoj Joshi", "Swati Desai", "Karan Mehta", "Ritu Nair",
            "Vishal Malhotra", "Priyanka Iyer", "Nikhil Bhatt", "Divya Kulkarni",
            "Akash Pandey", "Shruti Agarwal", "Rohan Mishra", "Tanvi Shah"
        ]
        
        roles = ['citizen', 'officer', 'registrar']
        role_weights = [0.7, 0.2, 0.1]  # More citizens, some officers, few registrars
        
        users_added = 0
        
        for i in range(users_to_add):
            try:
                name = indian_names[i % len(indian_names)]
                first_name = name.split()[0].lower()
                last_name = name.split()[1].lower()
                
                # Generate unique email
                email = f"{first_name}.{last_name}{i+10}@example.com"
                
                # Check if email already exists
                if User.query.filter_by(email=email).first():
                    email = f"{first_name}{i+20}.{last_name}@example.com"
                
                # Random role
                import random
                role = random.choices(roles, weights=role_weights)[0]
                
                # Create user
                user = User(
                    full_name=name,
                    email=email,
                    role=role,
                    phone=f"+91{9000000000 + i + 100}",
                    address=f"{i+1} Sample Street, Mumbai, Maharashtra",
                    is_active=True
                )
                user.set_password('password123')  # Default password
                
                db.session.add(user)
                users_added += 1
                
                print(f"Added user {users_added}: {name} ({email}) - {role}")
                
                # Commit every 5 users
                if users_added % 5 == 0:
                    db.session.commit()
            
            except Exception as e:
                print(f"Error adding user {i+1}: {str(e)}")
                db.session.rollback()
        
        # Final commit
        db.session.commit()
        
        # Verify final count
        final_count = User.query.count()
        print(f"\n✅ Successfully added {users_added} users!")
        print(f"📊 Total users in database: {final_count}")
        
        # Show breakdown by role
        print("\nUser role breakdown:")
        for role in ['admin', 'registrar', 'officer', 'citizen']:
            count = User.query.filter_by(role=role).count()
            print(f"  - {role}: {count}")
        
        print("\n🎉 Database updated successfully!")

if __name__ == '__main__':
    add_users()
