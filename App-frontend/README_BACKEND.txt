README.txt

==========================
Resume Analyzer - Backend
==========================

Description:
------------
This backend provides RESTful APIs for user management (registration, login, password reset) for the Resume Analyzer application.

Tech Stack:
-----------
- Java (Spring Boot)
- RESTful API
- Database (MySQL, PostgreSQL, or H2 for testing)

How to Run:
-----------
1. Configure your database connection in `application.properties`.
2. Build the project:
   mvn clean install
3. Run the backend server:
   mvn spring-boot:run
   or
   java -jar target/your-backend-app.jar

API Endpoints:
--------------

User Management:
----------------
- POST /api/user/add  
  Add a new user.  
  Body:  
  `{ "username": "string", "email": "string", "password": "string" }`

- POST /api/user/search  
  Search for a user by username/email and password (for login).  
  Body:  
  `{ "username": "string", "password": "string" }`  
  or  
  `{ "email": "string", "password": "string" }`

- POST /api/user/search  
  Search for a user by email (for password reset).  
  Body:  
  `{ "email": "string" }`

Notes:
------
- The backend runs by default on http://localhost:8081.
- Update CORS settings if you access the backend from a different domain/port.
- For production, configure security and environment variables properly.



Dependencies:
--------------sudo apt install xterm konsole xfce4-terminal -y