# FindIt — Lost & Found DBMS Project

This is a ready-to-run classroom project. You do not need to write code or create the database yourself.

## Included features
- Responsive website home page
- Register and login
- Report lost and found items
- Search item name, description, and location
- View item details and submit claims
- View your own reports
- Admin panel to update report status and approve/reject claims
- SQLite database is created automatically
- Sample reports are added for demonstration

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Internet connection only during initial Flask installation (unless Flask is already installed)

## Windows setup
1. Install Python from https://www.python.org/downloads/windows/
2. During installation, tick "Add python.exe to PATH".
3. Extract this ZIP.
4. Open the extracted folder.
5. Click the folder address bar, type `cmd`, and press Enter.
6. Run these commands one by one:
   ```
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```
7. Open Chrome and visit http://127.0.0.1:5000
8. Keep Command Prompt open while using the website. Press Ctrl+C to stop the server.

## Demo accounts
Student: student@demo.com / student123
Admin: admin@demo.com / admin123

These simple passwords are for classroom demo only. Do not use this version for real sensitive data or public internet deployment.

## Database design
### USERS
- id: Primary key
- name
- email: Unique
- password
- role: student/admin

### ITEMS
- id: Primary key
- user_id: Foreign key to USERS
- item_type: Lost/Found
- title, category, description, location, event_date, contact
- status: Open/Claim Pending/Resolved

### CLAIMS
- id: Primary key
- item_id: Foreign key to ITEMS
- user_id: Foreign key to USERS
- message
- status: Pending/Approved/Rejected

## SQL concepts demonstrated
- CREATE TABLE: creates tables
- INSERT: saves users, reports, and claims
- SELECT: reads database records
- WHERE and LIKE: searches records
- JOIN: combines claims with item and user details
- UPDATE: changes status
- PRIMARY KEY and FOREIGN KEY: connect records
- UNIQUE: prevents duplicate registered email addresses

## Project report
A ready-to-edit project report outline and viva Q&A are included in `docs/PROJECT_REPORT_AND_VIVA.md`.
An ER diagram is included in `docs/ER_DIAGRAM.md`.

## Notes
This is a beginner academic demo. It uses simple plain-text demo passwords to keep the code easy to understand; it is not secure for real users. It does not include email verification, image uploads, password reset, or production security. Do not publish real sensitive contact details.
