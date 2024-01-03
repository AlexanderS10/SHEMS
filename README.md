# SHEMS (Smart Home Energy Management System)
A website project for the course Principles of Database Systems simulating a home energy customer panel.

**Stack:**
- Django
- PostgreSQL
- ChartJS
  
**Features:**

- Users can create accounts with an email
- Forget password uses Django built in features to use email for reset password link
- On successful login users can register locations and within each location they can register devices
- Devices can send energy reports to the database on any interval time.
- Users can view the energy consumption per location or per device:
    - Compare energy consumption of locations to others of similar size.
    - View consumption on a daily basis for the past x selected days.
    - View detailed energy consumption for the last 24 hours.
    - View the device or location's total daily consumption for a selected date.
    - Identify the highest energy reported to the system each year.
 - Users can change their password which will remain hashed for security purposes.


**Security:**

Due to the time to develop the site Django built in features were used to implement security. 
- Hashed passwords
- Session based authentication. Although Token could be favored when scaling this is not an issue for this site project.
- CSRF Tokens are used on all data submission to prevent cross site forgery attacks.
- Templates with forms are used to protect as much as possible from XSS attacks.
- Paramentarized queries are used to prevent SQL Injections


**Requirements:**

Aside from the features another requirement is to use raw SQL queries when fetching data. As such as mentioned paramentarized
queries were implemented and fourtunately Django supports this. Additionally, transactions were used to protect the 
database from inconsistencies. 
The ORM was used at its minimum and only used to create the tables while all data fetching and updates are handled 
with raw SQL queries 
