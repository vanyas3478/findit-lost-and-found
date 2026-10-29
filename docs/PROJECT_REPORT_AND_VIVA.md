# LOST & FOUND MANAGEMENT SYSTEM
## DBMS Project Report — Editable Draft

**Submitted by:** ____________________  
**Roll Number:** ____________________  
**Course / Semester:** ____________________  
**Submitted to:** ____________________  
**College:** ____________________  
**Academic Session:** ____________________

---

## 1. Abstract
The Lost and Found Management System is a website designed to help people report and search for lost or found belongings. Users can register, log in, create reports, search listings, view item details, and submit claims. An administrator can review reports and update their status. The project uses HTML and CSS for the website interface, Python Flask for backend processing, and SQLite for storing records. The project demonstrates core DBMS operations such as INSERT, SELECT, UPDATE, JOIN, primary keys, and foreign keys. It runs locally on a computer and is suitable for a classroom demonstration.

## 2. Introduction
People often lose belongings such as identity cards, keys, books, wallets, and electronic devices in schools, colleges, offices, and public places. Finding the owner can be difficult when there is no central record. This project provides one local website where lost and found reports can be recorded and searched.

## 3. Problem Statement
Manual lost-and-found processes depend on notices, messages, and asking other people. Information can be missed, repeated, or become difficult to search. A database-based system can store reports in an organized form and make them easier to retrieve.

## 4. Objectives
- Create a user-friendly lost and found website.
- Allow users to register and log in.
- Save lost and found reports in a database.
- Search reports by item name, description, and location.
- Allow users to submit an ownership claim.
- Provide an admin page to manage report status and claims.
- Demonstrate practical database concepts.

## 5. Scope
The project is intended for a small college or campus demonstration. It supports local records and sample accounts. It can later be extended with image uploads, email notifications, better security, and online hosting.

## 6. Existing System
In a manual system, a person may contact a reception desk, post a notice, or send a message to a group. Searching old messages can be difficult and records may not be consistent.

## 7. Proposed System
The proposed system stores reports in a structured SQLite database. Users can search current reports through a website. Claims are saved for review, and the administrator can change the status of an item or claim.

## 8. Software and Hardware Requirements
**Software:** Windows 10/11, Python 3.10+, Flask, SQLite, HTML, CSS, web browser.  
**Hardware:** Laptop/desktop, approximately 4 GB RAM or more, and basic disk space.  
**Network:** Internet is required for the initial Flask installation if the package is not already available. The website itself runs offline after setup.

## 9. Modules
1. **Home and Search Module:** Displays open reports and allows keyword search.
2. **User Registration Module:** Creates a student account.
3. **Login Module:** Allows a registered user to access features.
4. **Report Module:** Saves a lost or found item.
5. **Item Details Module:** Displays an individual report.
6. **Claim Module:** Stores a claim message for an item.
7. **My Reports Module:** Shows the logged-in user's reports.
8. **Admin Module:** Updates item status and approves or rejects claims.

## 10. Database Design

### USERS table
| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | User name |
| email | TEXT | Unique email |
| password | TEXT | Demo password field |
| role | TEXT | student/admin |

### ITEMS table
| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to USERS |
| item_type | TEXT | Lost or Found |
| title | TEXT | Item name |
| category | TEXT | Item category |
| description | TEXT | Item details |
| location | TEXT | Lost/found location |
| event_date | TEXT | Date lost/found |
| contact | TEXT | Contact information |
| status | TEXT | Open/Claim Pending/Resolved |

### CLAIMS table
| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| item_id | INTEGER | Foreign key to ITEMS |
| user_id | INTEGER | Foreign key to USERS |
| message | TEXT | Claim explanation |
| status | TEXT | Pending/Approved/Rejected |

## 11. ER Diagram
Refer to `ER_DIAGRAM.md`. USERS has a one-to-many relationship with ITEMS. USERS has a one-to-many relationship with CLAIMS. ITEMS has a one-to-many relationship with CLAIMS.

## 12. SQL Concepts Used
- `CREATE TABLE` creates database tables.
- `INSERT INTO` saves users, reports, and claims.
- `SELECT` reads records from the database.
- `WHERE` filters records.
- `LIKE` searches partial text.
- `JOIN` combines related records.
- `UPDATE` changes item and claim status.
- `PRIMARY KEY` uniquely identifies each record.
- `FOREIGN KEY` links records across tables.
- `UNIQUE` prevents duplicate user emails.

## 13. Testing

| Test | Action | Expected result |
|---|---|---|
| 1 | Open home page | Sample items appear |
| 2 | Search “ID Card” | Matching item appears |
| 3 | Log in with demo student | User is logged in |
| 4 | Submit a lost-item report | Report is saved and shown |
| 5 | Open My Reports | User's reports appear |
| 6 | Log in as admin | Admin page opens |
| 7 | Change an item status | New status is saved |
| 8 | Submit a claim from another account | Claim is saved for admin review |

## 14. Limitations
This is a classroom prototype. It does not have image uploads, email verification, password recovery, advanced identity verification, or production-level security. The demo uses simple passwords to keep the code easy to explain and must not be used for real sensitive information or exposed to the public internet.

## 15. Future Scope
- Add photos of lost/found items.
- Add email notifications.
- Add stronger password security and password reset.
- Add filters for category and date.
- Add campus-specific user verification.
- Host securely on an internal college network.

## 16. Conclusion
The Lost and Found Management System provides a structured way to record and search for lost and found belongings. It combines a website interface with a database and demonstrates important DBMS operations. It is suitable for learning and classroom demonstration.

## 17. Bibliography
- Python documentation: https://docs.python.org/3/
- Flask documentation: https://flask.palletsprojects.com/
- SQLite documentation: https://www.sqlite.org/docs.html
- HTML reference: https://developer.mozilla.org/en-US/docs/Web/HTML
- CSS reference: https://developer.mozilla.org/en-US/docs/Web/CSS

---

# Viva Questions and Answers

**Q1. What is DBMS?**  
A DBMS is software used to store, organize, retrieve, and manage data.

**Q2. What is the purpose of this project?**  
It helps users report lost or found items and search the reports.

**Q3. Which database is used?**  
SQLite, a lightweight database stored in a local file.

**Q4. What is a primary key?**  
A primary key uniquely identifies each row in a table.

**Q5. What is a foreign key?**  
A foreign key connects a record in one table to a record in another table.

**Q6. Why are there three tables?**  
USERS stores accounts, ITEMS stores reports, and CLAIMS stores ownership claims. Separating them reduces repeated data and represents their relationships.

**Q7. What is SQL?**  
SQL stands for Structured Query Language. It is used to create, read, update, and delete database records.

**Q8. What does SELECT do?**  
SELECT retrieves records from a table.

**Q9. What does INSERT do?**  
INSERT adds a new record to a table.

**Q10. What does UPDATE do?**  
UPDATE changes existing records, such as an item's status.

**Q11. What is a JOIN?**  
JOIN combines related data from two or more tables.

**Q12. What is Flask?**  
Flask is a small Python web framework that connects website pages to backend code.

**Q13. What is HTML?**  
HTML defines the structure and content of a webpage.

**Q14. What is CSS?**  
CSS controls the appearance and layout of a webpage.

**Q15. Why use SQLite?**  
It is easy to set up and stores the database in a local file without a separate database server.

**Q16. What is the difference between Lost and Found reports?**  
A Lost report describes an item the user cannot find; a Found report describes an item the user has discovered.

**Q17. What is the role of an administrator?**  
The administrator reviews claims and changes report status.

**Q18. Does the project need internet after setup?**  
No. The local website works offline after Python and Flask are installed.

**Q19. What are the limitations?**  
The prototype does not include photo uploads, email notifications, or production-level security.

**Q20. What could be added in future?**  
Photo uploads, email notifications, secure password handling, advanced filters, and secure hosting.
