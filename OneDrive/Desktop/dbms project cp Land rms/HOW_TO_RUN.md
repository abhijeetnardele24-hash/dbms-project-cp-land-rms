# How to Run Land Registry Management System

## 📋 Prerequisites

Before running the project, ensure you have:
- ✅ Python 3.8+ installed
- ✅ MySQL Server running (with password: 1234)
- ✅ Database `land_registry_db` created
- ✅ All dependencies installed

---

## 🚀 Method 1: Running from Command Prompt / PowerShell (Without Warp)

### Step 1: Open Command Prompt or PowerShell
- Press `Win + R`, type `cmd` or `powershell`, press Enter
- OR right-click Start menu → Terminal/PowerShell

### Step 2: Navigate to Project Directory
```cmd
cd "C:\Users\Abhijeet Nardele\OneDrive\Desktop\dbms project cp Land rms"
```

### Step 3: Activate Virtual Environment (if using)
**For Command Prompt:**
```cmd
venv\Scripts\activate
```

**For PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get execution policy error in PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Set Database Environment Variable

**For Command Prompt:**
```cmd
set DATABASE_URL=mysql+pymysql://root:1234@localhost/land_registry_db
```

**For PowerShell:**
```powershell
$env:DATABASE_URL = "mysql+pymysql://root:1234@localhost/land_registry_db"
```

### Step 5: Run the Application
```cmd
python run.py
```

### Step 6: Open in Browser
- Open your web browser
- Go to: **http://127.0.0.1:5000**
- OR: **http://localhost:5000**

---

## 🎯 Method 2: Running with Batch File (Easiest for Windows)

### Create a Run Script

Create a file named `start_app.bat` in the project folder with this content:

```batch
@echo off
echo ====================================
echo  Land Registry Management System
echo ====================================
echo.

REM Set database URL
set DATABASE_URL=mysql+pymysql://root:1234@localhost/land_registry_db

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Running without virtual environment
)

echo.
echo Starting Flask application...
echo Open browser at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py

pause
```

**To run:** Just double-click `start_app.bat`

---

## 🔧 Method 3: Using Flask Environment Variables

### Create a `.env` file (Already exists)
The project already has a `.env` file with:
```
DATABASE_URL=mysql+pymysql://root:1234@localhost/land_registry_db
FLASK_APP=run.py
FLASK_ENV=development
```

### Install python-dotenv (if not installed)
```cmd
pip install python-dotenv
```

### Run directly
```cmd
python run.py
```

---

## 🌐 Method 4: Running in Production Mode

### For Development (with debug):
```cmd
set FLASK_ENV=development
python run.py
```

### For Production:
```cmd
set FLASK_ENV=production
python run.py
```

---

## 📝 Common Issues and Solutions

### Issue 1: "Module not found" Error
**Solution:**
```cmd
pip install -r requirements.txt
```

### Issue 2: "Can't connect to MySQL server"
**Solution:**
1. Check MySQL is running:
   - Open Services (Win + R → `services.msc`)
   - Find MySQL service and ensure it's running
2. Verify password is `1234`
3. Check database exists:
   ```sql
   mysql -u root -p
   SHOW DATABASES;
   ```

### Issue 3: "Port 5000 already in use"
**Solution - Change port in run.py:**
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

### Issue 4: PostgreSQL Dialect Error
**Solution:**
```cmd
set DATABASE_URL=mysql+pymysql://root:1234@localhost/land_registry_db
```
Make sure to set this EVERY TIME before running.

---

## 🎓 Quick Start Commands

### Windows Command Prompt:
```cmd
cd "C:\Users\Abhijeet Nardele\OneDrive\Desktop\dbms project cp Land rms"
set DATABASE_URL=mysql+pymysql://root:1234@localhost/land_registry_db
python run.py
```

### Windows PowerShell:
```powershell
cd "C:\Users\Abhijeet Nardele\OneDrive\Desktop\dbms project cp Land rms"
$env:DATABASE_URL = "mysql+pymysql://root:1234@localhost/land_registry_db"
python run.py
```

---

## 🔐 Default Login Credentials

### Admin
- Email: `admin@lrms.com`
- Password: `admin123`

### Registrar
- Email: `registrar@lrms.com`
- Password: `registrar123`

### Officer
- Email: `officer@lrms.com`
- Password: `officer123`

### Citizen
- Email: `user@lrms.com`
- Password: `user123`

---

## 📊 Testing the Application

### 1. Register a Property (Citizen)
- Login as citizen
- Go to "Register Property"
- Fill form with GPS coordinates (use map)
- Submit

### 2. Approve Property (Registrar)
- Login as registrar
- Go to "Pending Registrations"
- Click property → Approve
- ULPIN will be auto-generated

### 3. Submit Mutation (Citizen)
- Login as citizen
- Go to "Submit Mutation"
- Select approved property
- Fill form and submit

### 4. Approve Mutation (Officer)
- Login as officer
- Go to "Pending Mutations"
- Review and approve

### 5. Make Payment (Citizen)
- Login as citizen
- Go to "Make Payment"
- Select property and payment type
- Complete payment via Razorpay simulation

### 6. Verify in Database
Open MySQL Workbench:
```sql
USE land_registry_db;

-- Check properties
SELECT id, ulpin, village_city, status, created_at 
FROM properties 
ORDER BY created_at DESC;

-- Check payments
SELECT payment_reference, amount, status, payment_date 
FROM payments 
ORDER BY payment_date DESC;
```

---

## 🛑 Stopping the Application

- Press **Ctrl + C** in the terminal
- Wait for graceful shutdown
- Close terminal window

---

## 📦 Creating Desktop Shortcut

1. Right-click on `start_app.bat`
2. Click "Send to" → "Desktop (create shortcut)"
3. Rename shortcut to "Land Registry System"
4. Double-click shortcut to run anytime

---

## 🔄 Restarting After Changes

If you modify code:
1. Press Ctrl + C to stop
2. Run `python run.py` again
3. Refresh browser (Ctrl + F5)

In development mode with debug=True, Flask auto-reloads on code changes!

---

## 📞 Need Help?

### Check Logs
Application logs errors to console. Look for:
- Red error messages
- Traceback information
- SQL query errors

### Verify Database Connection
```cmd
python verify_database.py
```

### Run All Verifications
```cmd
python verify_all_forms.py
```

---

## ✅ Success Indicators

When running correctly, you should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

**Now open http://127.0.0.1:5000 in your browser!**

---

## 🎉 Project is Ready!

Your Land Registry Management System is now running with:
- ✅ MySQL database (password: 1234)
- ✅ All forms working and verified
- ✅ Property registration with GPS
- ✅ Interactive Leaflet maps
- ✅ Payment processing with Razorpay
- ✅ Dashboard with Chart.js
- ✅ All user roles functional
- ✅ Data persistence verified

**Enjoy your Land Registry Management System! 🏠📋**
