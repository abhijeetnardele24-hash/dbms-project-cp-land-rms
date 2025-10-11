# Land Records Management System (LRMS)

A comprehensive Flask-based web application for managing land parcels, ownership records, mutations, and tax assessments.

## Features

- **User Authentication**: Role-based access control (Admin, Registrar, Approver, Viewer)
- **Parcel Management**: Complete CRUD operations for land parcels
- **Ownership Tracking**: Manage ownership records with share fractions
- **Mutation Processing**: Handle property transfers with approval workflow
- **Tax Assessment**: Track tax assessments and payments
- **Document Management**: Store and link legal documents
- **Audit Trail**: Complete audit logging for all operations
- **Responsive UI**: Modern Bootstrap 5 interface

## Tech Stack

- **Backend**: Python 3.8+, Flask 2.3+
- **Database**: MySQL 8.0+ with SQLAlchemy ORM (Primary), SQLite (Development)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **Database Connector**: PyMySQL for MySQL connectivity
- **Other**: Flask-CORS, Flask-SQLAlchemy

## Installation

### Prerequisites

1. Python 3.8 or higher
2. MySQL 8.0 or higher
3. pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   cd /path/to/your/projects
   git clone <repository-url>
   cd lrms
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL Database**
   
   **Option 1: Using the provided SQL script**
   ```bash
   mysql -u root -p < setup_mysql.sql
   ```
   
   **Option 2: Manual setup**
   ```sql
   mysql -u root -p
   CREATE DATABASE lrms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'lrms_user'@'localhost' IDENTIFIED BY 'lrms_password';
   GRANT ALL PRIVILEGES ON lrms.* TO 'lrms_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Configure Database Connection**
   
   **Option 1: Use default configuration (root user)**
   The default config uses: `mysql+pymysql://root:password@localhost/lrms`
   Make sure your MySQL root password matches or update `config.py`
   
   **Option 2: Use environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=mysql+pymysql://lrms_user:lrms_password@localhost/lrms
   SECRET_KEY=your-secret-key-here
   FLASK_DEBUG=True
   ```

6. **Test Database Connection (Optional)**
   ```bash
   python test_db_connection.py
   ```
   This will verify your MySQL connection is working properly.

7. **Initialize Database**
   ```bash
   python app.py
   ```
   The application will automatically create all MySQL tables and a default admin user.

8. **Access the Application**
   - Open your browser and go to `http://localhost:5001`
   - Login with default credentials:
     - Username: `admin`
     - Password: `admin123`

## Database Schema

The system includes 12 main entities:

1. **owner** - Property owners (individuals, companies, government)
2. **user_account** - System users with role-based access
3. **location** - Geographic location details
4. **parcel** - Land parcel information
5. **parcel_version** - Historical versions of parcel boundaries
6. **ownership** - Ownership records with share fractions
7. **tenant_agreement** - Lease agreements
8. **mutation** - Property transfer records
9. **document** - Legal document storage
10. **encumbrance** - Liens, mortgages, disputes
11. **tax_assessment** - Tax calculations and payments
12. **audit_log** - Complete audit trail

## User Roles

- **Admin**: Full system access, user management
- **Registrar**: Create/edit parcels, owners, mutations
- **Approver**: Approve/reject mutations
- **Viewer**: Read-only access to all records

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /logout` - Logout user

### Dashboard
- `GET /dashboard` - Main dashboard with statistics

### Parcels
- `GET /parcel/` - List all parcels
- `GET /parcel/<id>` - View parcel details
- `GET /parcel/create` - Create new parcel form
- `POST /parcel/create` - Submit new parcel
- `GET /parcel/<id>/edit` - Edit parcel form
- `POST /parcel/<id>/edit` - Update parcel

### Owners
- `GET /owner/` - List all owners
- `GET /owner/<id>` - View owner details
- `GET /owner/create` - Create new owner form
- `POST /owner/create` - Submit new owner
- `GET /owner/api/search` - Search owners API

### Mutations
- `GET /mutation/` - List all mutations
- `GET /mutation/<id>` - View mutation details
- `GET /mutation/create` - Create new mutation form
- `POST /mutation/create` - Submit new mutation
- `POST /mutation/<id>/approve` - Approve mutation
- `POST /mutation/<id>/reject` - Reject mutation

### Tax Assessments
- `GET /tax/` - List all tax assessments
- `GET /tax/<id>` - View tax assessment details
- `GET /tax/create` - Create new assessment form
- `POST /tax/create` - Submit new assessment
- `GET /tax/<id>/payment` - Record payment form
- `POST /tax/<id>/payment` - Submit payment

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- CSRF protection
- SQL injection prevention through SQLAlchemy ORM

## Development

### Running in Development Mode
```bash
export FLASK_DEBUG=True
python app.py
```

### Database Migrations
The application uses SQLAlchemy's `create_all()` method for initial setup. For production, consider using Flask-Migrate for database migrations.

### Adding New Features
1. Create new models in `models/`
2. Add routes in `routes/`
3. Create templates in `templates/`
4. Update the main `app.py` to register new blueprints

## Production Deployment

1. Set `FLASK_DEBUG=False`
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure proper database connection pooling
4. Set up SSL/TLS certificates
5. Configure proper logging
6. Set strong secret keys and passwords

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL service is running
   - Verify database credentials in config
   - Ensure database exists

2. **Import Errors**
   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

3. **Permission Errors**
   - Check file permissions
   - Ensure upload directory is writable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please create an issue in the repository or contact the development team.
