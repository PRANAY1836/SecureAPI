# SecureAPI — Application Security & VAPT Lab

> A deliberately security-focused Flask REST API used to practice application security testing, vulnerability assessment, remediation, and retesting.

---

## 1. Project Overview

**SecureAPI** is a local Flask-based REST API security laboratory designed to demonstrate practical Application Security and Vulnerability Assessment and Penetration Testing (VAPT) concepts.

The project follows a complete security testing lifecycle:

```text
Build API
   |
   v
Identify Attack Surface
   |
   v
Perform Security Testing
   |
   v
Identify Vulnerabilities
   |
   v
Analyze Root Cause
   |
   v
Implement Remediation
   |
   v
Retest
   |
   v
Document Findings
```

The application was intentionally designed as a controlled environment where common API security weaknesses could be studied safely.

---

## 2. Objectives

The main objectives of this project are:

- Understand REST API security.
- Implement authentication using JWT.
- Implement password hashing.
- Understand authentication vs authorization.
- Test object-level authorization.
- Study BOLA/IDOR vulnerabilities.
- Identify and remediate SQL Injection.
- Implement parameterized SQL queries.
- Analyze HTTP security headers.
- Implement API rate limiting.
- Perform controlled security testing using Postman.
- Retest vulnerabilities after remediation.
- Document findings using a professional VAPT report.

---

## 3. Security Areas Tested

The project focuses on the following application-security areas:

| Security Area | Testing / Control |
|---|---|
| Authentication | JWT-based authentication |
| Password Security | Password hashing |
| Authorization | Object-level authorization |
| API Security | Protected REST endpoints |
| BOLA / IDOR | Cross-object authorization testing |
| SQL Injection | Controlled injection testing |
| Database Security | Parameterized queries |
| HTTP Security | Security headers |
| API Abuse | Rate limiting |
| Security Testing | Postman |
| Reporting | VAPT documentation |

---

## 4. Vulnerabilities and Security Improvements

The project covered the following security findings:

| ID | Finding | Severity | Status |
|---|---|---|---|
| SEC-001 | Broken Object Level Authorization (BOLA/IDOR) | High | Fixed |
| SEC-002 | SQL Injection | High | Fixed |
| SEC-003 | Missing Security Headers | Low/Medium | Fixed |
| SEC-004 | Missing Rate Limiting | Medium | Fixed |

### Security Testing Approach

Each security issue followed the same basic process:

```text
Vulnerability
     |
     v
Security Test
     |
     v
Root Cause Analysis
     |
     v
Remediation
     |
     v
Retest
     |
     v
Verification
```

---

## 5. Key Features

### Authentication

- JWT-based authentication
- Login endpoint
- Bearer token authentication
- Protected API endpoints
- Password hashing

### Authorization

- Object-level authorization
- User identity validation
- Unauthorized object access protection
- HTTP `403 Forbidden` response

### Database Security

- SQLite database
- Parameterized SQL queries
- SQL Injection testing
- SQL Injection remediation

### API Hardening

- HTTP security headers
- Login rate limiting
- HTTP status-code handling
- Controlled error responses

### Security Testing

- Manual API testing
- Authentication testing
- Authorization testing
- Injection testing
- Header inspection
- Rate-limit testing
- Retesting after remediation

---

## 6. Technology Stack

```text
Backend       : Python + Flask
Database      : SQLite
Authentication: JWT
Password      : Werkzeug
Rate Limiting : Flask-Limiter
Testing       : Postman
IDE           : Visual Studio Code
Version Ctrl  : Git
Repository    : GitHub
```

## 7. Application Architecture

The SecureAPI application follows a simple REST API architecture.

```text
                   Client
                     |
             +-------+-------+
             |               |
          Postman          Browser
             |               |
             +-------+-------+
                     |
                     v
              Flask REST API
                     |
          +----------+----------+
          |                     |
          v                     v
   Authentication          API Endpoints
          |                     |
          v                     v
        JWT              Authorization
                                |
                                v
                         Database Layer
                                |
                                v
                           SQLite DB
```

---

## 8. Security Architecture

Security controls are implemented at multiple layers of the application.

```text
+--------------------------------------------------+
|                    SecureAPI                     |
+--------------------------------------------------+
|                                                  |
|  Authentication                                  |
|  └── JWT                                         |
|                                                  |
|  Authorization                                   |
|  └── Object-Level Authorization                  |
|                                                  |
|  Database Security                               |
|  └── Parameterized SQL Queries                   |
|                                                  |
|  API Hardening                                   |
|  ├── Security Headers                             |
|  └── Rate Limiting                               |
|                                                  |
|  Password Security                               |
|  └── Password Hashing                            |
|                                                  |
+--------------------------------------------------+
```

The project follows a defense-in-depth approach where multiple security controls protect different parts of the application.

---

## 9. API Endpoints

The application exposes several REST API endpoints.

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| GET | `/` | API information | No |
| POST | `/api/login` | User authentication | No |
| GET | `/api/users` | Retrieve users | Protected |
| GET | `/api/users/<id>` | Retrieve a specific user | Protected |
| GET | `/api/search` | Search users | API endpoint testing |

---

## 10. Authentication Workflow

The authentication process works as follows:

```text
                    User
                      |
                      | Email + Password
                      v
                 POST /api/login
                      |
                      v
              Verify Credentials
                      |
              +-------+-------+
              |               |
           Invalid           Valid
              |               |
              v               v
        401 Unauthorized    Generate JWT
                              |
                              v
                         Return Token
                              |
                              v
                    Client Sends JWT
                              |
                              v
                    Protected Endpoint
```

### Example Login Request

```http
POST /api/login
Content-Type: application/json
```

```json
{
    "email": "pranay@example.com",
    "password": "<YOUR_LOCAL_TEST_PASSWORD>"
}
```

A successful login returns a JWT that can be used to access protected endpoints.

---

## 11. Authorization Workflow

Authorization is performed after authentication.

```text
Request
   |
   v
JWT Validation
   |
   v
Authenticated User
   |
   v
Requested Object
   |
   v
Authorization Check
   |
   +----------+----------+
   |                     |
 Authorized          Unauthorized
   |                     |
   v                     v
200 OK              403 Forbidden
```

This prevents a valid authenticated user from automatically accessing every object in the application.

---

## 12. SQL Injection Testing Workflow

The SQL Injection assessment followed a controlled process.

### Initial Vulnerable Query

```python
query = "SELECT id, name, email FROM users WHERE name = '" + name + "'"
```

### Test Input

```text
' OR '1'='1
```

### Vulnerable Flow

```text
User Input
    |
    v
SQL String Concatenation
    |
    v
Modified SQL Query
    |
    v
Database
    |
    v
Multiple Records Returned
```

### Remediated Flow

```text
User Input
    |
    v
Parameterized Query
    |
    v
Database
    |
    v
Input Treated as Data
    |
    v
Injection Prevented
```

### Secure Query

```python
query = "SELECT id, name, email FROM users WHERE name = ?"

users = connection.execute(query, (name,)).fetchall()
```

---

## 13. Rate Limiting Workflow

The login endpoint uses Flask-Limiter.

```text
Client
  |
  v
POST /api/login
  |
  v
Rate Limit Check
  |
  +-------------------+
  |                   |
 Within Limit     Limit Exceeded
  |                   |
  v                   v
Process Request    429 Response
```

Configured limit:

```text
5 requests per minute
```

This provides a basic control against excessive authentication attempts.

---

## 14. Security Testing Tools

### Postman

Postman was used for manual API security testing.

Testing included:

- Sending API requests
- Testing authentication
- Supplying JWT tokens
- Testing authorization
- Sending SQL Injection payloads
- Inspecting response headers
- Testing rate limiting
- Verifying HTTP status codes

### Visual Studio Code

VS Code was used for:

- Source-code development
- Security-control implementation
- Vulnerability remediation
- Debugging
- Report creation

### Git and GitHub

Git and GitHub are used for:

- Version control
- Source-code management
- Project documentation
- Security-project portfolio presentation

---

## 15. Project Structure

The project is organized as follows:

```text
SecureAPI/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── VAPT-Report.md
├── .gitignore
├── .env
└── secureapi.db
```

### Important Security Note

The `.env` file contains environment-specific configuration and should not be committed to GitHub.

The `.gitignore` file is configured to prevent sensitive local configuration from being uploaded.

```text
.env
```

is intentionally excluded from version control.

---

## 16. VAPT Report

A detailed security assessment report is included in:

```text
VAPT-Report.md
```

The report contains:

- Executive Summary
- Scope
- Methodology
- Findings Summary
- Vulnerability Details
- Severity
- Affected Endpoints
- Security Testing
- Root Cause Analysis
- Remediation
- Retesting
- Security Verification
- Recommendations
- Lessons Learned

## 17. Security Testing Results

The application was tested before and after security controls were implemented.

### Results Summary

| Test | Security Issue | Remediation | Retest |
|---|---|---|---|
| Object-level authorization | BOLA/IDOR risk | Authorization check | Passed |
| SQL Injection | SQL query manipulation | Parameterized query | Passed |
| Security headers | Missing hardening headers | Added security headers | Passed |
| Rate limiting | Unlimited login attempts | Flask-Limiter | Passed |

---

## 18. Example Security Tests

### Test 1 — Unauthorized Object Access

```http
GET /api/users/2
```

Authenticated user:

```text
User ID: 1
```

Expected security behavior:

```text
403 Forbidden
```

Result:

```text
403 Forbidden
```

---

### Test 2 — SQL Injection

Payload:

```text
' OR '1'='1
```

Endpoint:

```text
GET /api/search
```

After remediation:

```text
[]
```

The input was treated as data rather than executable SQL syntax.

---

### Test 3 — Security Headers

Verified headers:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

---

### Test 4 — Rate Limiting

Configured:

```text
5 requests per minute
```

After exceeding the limit:

```text
429 Too Many Requests
```

---

## 19. Security Testing Methodology

The testing methodology used in this project can be summarized as:

### Phase 1 — Reconnaissance

Identify the application's:

- API endpoints
- Authentication mechanism
- Database
- User-controlled inputs
- Security controls

### Phase 2 — Security Testing

Test:

- Authentication
- Authorization
- Object-level access
- Input handling
- SQL Injection
- HTTP headers
- Request-rate controls

### Phase 3 — Vulnerability Analysis

For each finding:

- Identify the vulnerable component.
- Determine the root cause.
- Determine potential security impact.
- Assign an appropriate severity.

### Phase 4 — Remediation

Implement appropriate security controls.

### Phase 5 — Retesting

Repeat the original security test after remediation.

### Phase 6 — Documentation

Document:

- Vulnerability
- Severity
- Affected endpoint
- Evidence
- Root cause
- Remediation
- Retest result
- Recommendation

---

## 20. What This Project Demonstrates

This project demonstrates practical exposure to:

```text
Application Security
        |
        +-- REST API Security
        |
        +-- Authentication
        |
        +-- Authorization
        |
        +-- JWT
        |
        +-- Password Security
        |
        +-- BOLA / IDOR
        |
        +-- SQL Injection
        |
        +-- Secure Database Queries
        |
        +-- HTTP Security Headers
        |
        +-- Rate Limiting
        |
        +-- Vulnerability Remediation
        |
        +-- Security Retesting
        |
        +-- VAPT Reporting
```

---

## 21. Learning Outcomes

Through this project, the following concepts were practiced hands-on:

- Understanding API attack surfaces
- Identifying authentication requirements
- Understanding the difference between authentication and authorization
- Testing object-level authorization
- Understanding BOLA/IDOR
- Testing SQL Injection in a controlled environment
- Understanding parameterized SQL queries
- Inspecting HTTP response headers
- Implementing security headers
- Understanding rate limiting
- Testing HTTP `401`, `403`, and `429` responses
- Performing vulnerability remediation
- Conducting security retesting
- Writing technical security documentation

---

## 22. Responsible Disclosure and Testing

This project was developed as a controlled security-testing laboratory.

All vulnerability testing was performed against the locally hosted application:

```text
http://127.0.0.1:5000
```

The project does not target external systems, production applications, or third-party services.

Security testing was performed only against systems under direct control of the developer.

---

## 23. Future Improvements

The project can be extended with additional application-security testing and defensive controls.

Potential improvements include:

- Burp Suite testing
- OWASP ZAP testing
- Nmap reconnaissance
- Automated API security testing
- SAST integration
- DAST integration
- Dependency vulnerability scanning
- CI/CD security checks
- HTTPS/TLS configuration
- Secure cookie configuration
- CORS security configuration
- CSRF protection where applicable
- JWT expiration and refresh tokens
- Multi-factor authentication
- Account lockout controls
- Security logging
- Audit trails
- Centralized monitoring
- API gateway security

---

## 24. Project Status

```text
Application Development       : Completed
Authentication                : Implemented
Authorization                 : Implemented
SQL Injection Testing         : Completed
SQL Injection Remediation     : Completed
Security Header Hardening     : Completed
Rate Limiting                 : Implemented
Security Retesting            : Completed
VAPT Documentation            : Completed
GitHub Documentation          : Completed
```

---

## 25. Author

**Loya Pranay**

Computer Science Engineering Student

Areas of Interest:

- Application Security
- VAPT
- Cybersecurity
- REST API Security
- Software Development
- AI/ML

---

## 26. Disclaimer

SecureAPI is an educational cybersecurity project created for controlled application-security testing.

The vulnerabilities discussed in this repository are demonstrated only within the intentionally controlled local application environment.

Security testing should only be performed on systems for which appropriate authorization has been obtained.

---
## 27. Final Project Flow

```text
                 SECUREAPI
                     |
                     v
              Flask REST API
                     |
                     v
             Security Assessment
                     |
       +-------------+-------------+
       |             |             |
       v             v             v
 Authentication  Authorization   Input Testing
       |             |             |
       v             v             v
      JWT        BOLA/IDOR       SQL Injection
       |             |             |
       +-------------+-------------+
                     |
                     v
              Vulnerability Fixes
                     |
          +----------+----------+
          |                     |
          v                     v
   Security Headers       Rate Limiting
          |                     |
          +----------+----------+
                     |
                     v
                  Retesting
                     |
                     v
               VAPT Report
                     |
                     v
              Security Verified
```

---

# SecureAPI

**Build → Test → Exploit Safely → Fix → Retest → Document**

This project demonstrates the practical application-security mindset required to identify vulnerabilities, understand their root causes, implement defensive controls, and verify the effectiveness of remediation.
