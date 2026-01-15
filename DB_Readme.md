Database Explanation Document
This PDF explains the structure and purpose of the SQL database schema for the Lab
Complaint & ICC Management System.

1. USERS TABLE
- Stores all system users: students, technicians (lab assistants), ICC members, and admins.
- Uses ENUM for role to keep a single unified authentication system.
- Important fields: name, email (unique), password, role, department.
- Timestamps track account creation.

2. LABS TABLE
- Stores fixed lab list used for filing lab complaints.
- Contains Lab_ID and Lab_Name.

3. LAB_COMPLAINTS TABLE
- Stores complaints filed by students.
- Linked to USERS (filed by user) and LABS (location of issue).
- Assigned technician is also referenced via foreign key to USERS.
- Status uses ENUM to track progress.

4. ICC_COMPLAINTS TABLE
- Stores complaints filed under ICC module.
- Linked to USERS (complainant) and ICC_PANEL.
- Status uses ENUM to track case lifecycle.

5. ICC_PANEL TABLE
- Stores ICC panel information.
- Helps determine case assignment authority.

6. ICC_PANEL_MEMBERS TABLE
- Junction table linking ICC_PANEL and USERS.
- Supports multiple users per panel.

7. NOTIFICATIONS TABLE
- Stores system notifications for users.
- Helps backend send/read alert messages.

RELATIONSHIPS SUMMARY
- One User can file multiple Lab Complaints and ICC Complaints.
- One Lab can have multiple Lab Complaints.
- One ICC Panel can handle multiple ICC Complaints.
- ICC Panel Members supports many-to-many mapping between users and panels.
.Main SQL code is uploaded separately.
- This PDF serves as documentation for database structure, relationships, and design
decisions.