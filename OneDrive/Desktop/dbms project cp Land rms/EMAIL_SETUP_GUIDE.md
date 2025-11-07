# Email Alert Setup Guide 📧

## Overview
This guide explains how to configure and test the email notification system in your Land Registry Management System.

---

## 🎯 What Email Alerts Do

The system sends automatic email notifications for:

1. **Property Approval** - When registrar approves a property
2. **Mutation Status Updates** - When officer approves/rejects mutations
3. **Payment Receipts** - When payment is completed
4. **Welcome Emails** - When new users register (optional)

---

## 📋 Current Implementation Status

✅ **Email service code is ready** in `app/utils/email_service.py`  
✅ **Professional HTML templates** with styling  
✅ **Configuration setup** in `config.py`  
⚠️ **Email credentials NOT configured** (needs setup)

---

## 🛠️ Setup Methods

### **Option 1: Gmail (Recommended for Testing)**

#### Step 1: Enable App Password in Gmail

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** in the left panel
3. Enable **2-Step Verification** (if not already enabled)
4. Search for **App Passwords** 
5. Generate a new app password:
   - Select app: **Mail**
   - Select device: **Windows Computer** (or Other)
   - Click **Generate**
6. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

#### Step 2: Set Environment Variables

**Windows PowerShell:**
```powershell
# Set environment variables (temporary - for current session)
$env:MAIL_USERNAME = "your.email@gmail.com"
$env:MAIL_PASSWORD = "your-16-char-app-password"
$env:MAIL_DEFAULT_SENDER = "your.email@gmail.com"
```

**Windows Command Prompt:**
```cmd
set MAIL_USERNAME=your.email@gmail.com
set MAIL_PASSWORD=your-16-char-app-password
set MAIL_DEFAULT_SENDER=your.email@gmail.com
```

**For Permanent Setup (Windows):**
1. Search "Environment Variables" in Windows
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", click "New"
5. Add:
   - Variable name: `MAIL_USERNAME`, Value: `your.email@gmail.com`
   - Variable name: `MAIL_PASSWORD`, Value: `your-app-password`
   - Variable name: `MAIL_DEFAULT_SENDER`, Value: `your.email@gmail.com`

#### Step 3: Restart Flask App
```powershell
# Stop the current Flask app (Ctrl+C)
# Then restart it
python run.py
```

---

### **Option 2: Mailtrap (Recommended for Development)**

Mailtrap catches all emails in a fake inbox - perfect for testing!

1. **Sign up** at https://mailtrap.io/ (Free)
2. Go to **Email Testing** → **Inboxes**
3. Copy credentials from **SMTP Settings**
4. Set environment variables:

```powershell
$env:MAIL_SERVER = "sandbox.smtp.mailtrap.io"
$env:MAIL_PORT = "2525"
$env:MAIL_USERNAME = "your-mailtrap-username"
$env:MAIL_PASSWORD = "your-mailtrap-password"
$env:MAIL_USE_TLS = "true"
$env:MAIL_DEFAULT_SENDER = "test@lrms.com"
```

5. Restart Flask app
6. All emails will appear in your Mailtrap inbox!

---

### **Option 3: Console Output (Quick Testing)**

For quick testing without email setup, print emails to console:

Edit `app/utils/email_service.py`:

```python
# Add this at the top
TESTING_MODE = True  # Set to True for console output

@staticmethod
def send_property_approval_email(user_email, property_data):
    """Send email when property is approved"""
    if TESTING_MODE:
        print("=" * 60)
        print(f"📧 EMAIL TO: {user_email}")
        print(f"SUBJECT: Property Approved - {property_data.get('ulpin')}")
        print(f"Property: {property_data}")
        print("=" * 60)
        return True
    
    # ... existing email sending code ...
```

---

## 🧪 Testing Email Alerts

### Test 1: Property Approval Email

1. **Login as Registrar**
2. Go to **Pending Registrations**
3. **Approve a property**
4. Check email inbox (or Mailtrap or console)

**Expected Email:**
- Subject: "🎉 Property Approved - ULPIN-XXXXX"
- Professional HTML with property details
- Button to "View My Properties"

### Test 2: Mutation Status Email

1. **Login as Officer**
2. Go to **Pending Mutations**
3. **Approve or Reject** a mutation
4. Check applicant's email

**Expected Email:**
- Subject: "✅ Mutation Approved - MUT-XXXXX" (or ❌ for rejected)
- Status badge with color
- Mutation details and officer comments

### Test 3: Payment Receipt Email

1. **Login as Citizen**
2. **Make a payment**
3. Complete the payment
4. Check email

**Expected Email:**
- Subject: "💳 Payment Receipt - PAY-XXXXX"
- Receipt with amount in green
- Transaction details table

---

## 🔍 Troubleshooting

### Issue: "Connection refused" or "SMTP error"

**Solution:**
1. Check if email credentials are set:
   ```powershell
   echo $env:MAIL_USERNAME
   echo $env:MAIL_PASSWORD
   ```
2. Verify Gmail app password (not regular password)
3. Check firewall/antivirus blocking port 587

### Issue: "Authentication failed"

**Solution:**
1. Re-generate Gmail app password
2. Make sure 2-Step Verification is enabled
3. Use exact 16-character password (remove spaces)

### Issue: Emails not sending but no error

**Solution:**
1. Check Flask console for error messages
2. Verify `mail` object is initialized in `app/__init__.py`
3. Check if `mail.send(msg)` is actually called

### Issue: "SMTPServerDisconnected"

**Solution:**
```python
# Add retry logic in email_service.py
import time

def send_with_retry(msg, max_retries=3):
    for attempt in range(max_retries):
        try:
            mail.send(msg)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait 2 seconds
                continue
            print(f"Failed after {max_retries} attempts: {e}")
            return False
```

---

## 📝 Current Email Configuration (config.py)

```python
# Email configuration
MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')      # ⚠️ NEEDS SETUP
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')      # ⚠️ NEEDS SETUP
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@lrms.com'
```

---

## 🚀 Quick Start for Demo

**For Placement Demo (No Real Emails):**

1. Edit `app/utils/email_service.py` - Add at line 12:
   ```python
   DEMO_MODE = True  # Set to False to send real emails
   ```

2. Modify each email function to check DEMO_MODE:
   ```python
   @staticmethod
   def send_property_approval_email(user_email, property_data):
       if DEMO_MODE:
           print(f"✅ [DEMO] Email sent to {user_email}")
           return True
       # ... real email code ...
   ```

3. During demo, you can say:
   - "Emails are configured and would be sent to users"
   - "In production, users receive professional HTML emails"
   - "For this demo, we're printing to console"

---

## 📧 Email Templates Features

All email templates include:
- ✅ Professional HTML design with gradients
- ✅ Responsive layout (mobile-friendly)
- ✅ Color-coded status badges
- ✅ Direct action buttons
- ✅ Property/Mutation/Payment details
- ✅ Footer with copyright
- ✅ "Do not reply" notice

---

## 🔐 Security Best Practices

1. **Never commit credentials** to Git
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use App Passwords** (not regular Gmail password)

3. **Limit email rate** to avoid spam filters:
   ```python
   import time
   from functools import wraps
   
   def rate_limit(seconds=1):
       def decorator(func):
           @wraps(func)
           def wrapper(*args, **kwargs):
               time.sleep(seconds)
               return func(*args, **kwargs)
           return wrapper
       return decorator
   
   @rate_limit(2)  # 2 seconds between emails
   def send_email(...):
       pass
   ```

4. **Validate email addresses** before sending:
   ```python
   import re
   
   def is_valid_email(email):
       pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
       return re.match(pattern, email) is not None
   ```

---

## 🎓 For Placement Interview

**When explaining email feature:**

1. **Show the code**: Open `app/utils/email_service.py`
2. **Explain the flow**:
   - "When officer approves mutation..."
   - "Email service is called with user data..."
   - "Professional HTML template is rendered..."
   - "Email is sent via SMTP..."
3. **Show configuration**: Open `config.py`
4. **Demonstrate** (if emails are set up):
   - Approve a property/mutation
   - Show received email in inbox
5. **Mention security**:
   - "Using environment variables for credentials"
   - "App passwords for Gmail"
   - "TLS encryption for sending"

**Key Points to Highlight:**
- ✅ Professional HTML emails (not plain text)
- ✅ Asynchronous sending (doesn't block user)
- ✅ Error handling (graceful failure)
- ✅ Multiple email types (property, mutation, payment)
- ✅ Production-ready configuration

---

## 📦 Alternative: Create .env File

Create `.env` file in project root:

```env
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your.email@gmail.com

# Database
DATABASE_URL=mysql+pymysql://root:1234@localhost/land_registry_db

# Secret Key
SECRET_KEY=your-secret-key-change-in-production
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

Add to `config.py` (top of file):
```python
from dotenv import load_dotenv
load_dotenv()  # Load .env file
```

---

## ✅ Verification Checklist

Before demo/production:
- [ ] Email credentials configured
- [ ] Environment variables set
- [ ] Flask app restarted
- [ ] Test email sent successfully
- [ ] HTML renders correctly
- [ ] Links in email work
- [ ] Error handling works (test with wrong credentials)
- [ ] Emails appear professional

---

**Quick Test Command:**
```python
# In Flask shell
python
>>> from app import create_app, mail
>>> from flask_mail import Message
>>> app = create_app()
>>> with app.app_context():
...     msg = Message("Test Email", recipients=["your.email@gmail.com"])
...     msg.body = "This is a test"
...     mail.send(msg)
>>> # Check your inbox!
```

---

**Status**: Ready to configure! Just add email credentials. 📧  
**Recommendation**: Use Mailtrap for development/testing, Gmail for production.
