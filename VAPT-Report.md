# SecureAPI — VAPT Security Assessment Report

## 1. Executive Summary

SecureAPI is a Flask-based REST API developed as an application-security testing laboratory.

The assessment focused on authentication, authorization, API security, database security, HTTP security headers, and request-rate controls.

The assessment covered the following security areas:

- Authentication testing
- Authorization testing
- API endpoint testing
- SQL Injection testing
- HTTP security header assessment
- Rate-limit testing
- Vulnerability remediation
- Security retesting

The project demonstrates a practical Vulnerability Assessment and Penetration Testing (VAPT) workflow in a controlled local environment.

The identified security weaknesses were remediated and subsequently re-tested to verify the effectiveness of the implemented controls.

---

## 2. Scope

### Application

**SecureAPI REST API**

### Environment

- Python
- Flask
- SQLite
- JWT
- Flask-Limiter
- Postman
- Visual Studio Code

### Testing Environment

```text
http://127.0.0.1:5000
```

### Testing Type

- Authentication testing
- Authorization testing
- API security testing
- SQL Injection testing
- HTTP security header assessment
- Rate-limit testing
- Vulnerability remediation
- Retesting

---

## 3. Methodology

The security assessment followed a structured VAPT methodology.

### Assessment Process

```text
Reconnaissance
      |
      v
Endpoint Identification
      |
      v
Authentication Testing
      |
      v
Authorization Testing
      |
      v
Input Validation Testing
      |
      v
Vulnerability Identification
      |
      v
Remediation
      |
      v
Retesting
      |
      v
Security Verification
```

### Methodology Steps

1. **Application Reconnaissance**  
   Identified the application, available endpoints, authentication mechanisms, and general API behavior.

2. **Endpoint Identification**  
   Identified API endpoints such as login, user retrieval, and search functionality.

3. **Authentication Testing**  
   Tested login functionality and JWT-based authentication.

4. **Authorization Testing**  
   Tested whether authenticated users could access objects belonging to other users.

5. **Input Validation Testing**  
   Tested user-controlled input for potential injection vulnerabilities.

6. **SQL Injection Testing**  
   Performed controlled SQL Injection testing against the search endpoint.

7. **Security Header Assessment**  
   Inspected HTTP response headers and identified missing security-hardening headers.

8. **Rate-Limit Testing**  
   Repeated authentication requests to determine whether excessive login attempts were restricted.

9. **Remediation**  
   Implemented appropriate security controls for the identified weaknesses.

10. **Retesting**  
    Repeated the security tests after remediation to verify that the controls were effective.

---

# 4. Findings Summary

| ID | Vulnerability | Severity | Status |
|---|---|---|---|
| SEC-001 | Broken Object Level Authorization (BOLA/IDOR) | High | Fixed |
| SEC-002 | SQL Injection | High | Fixed |
| SEC-003 | Missing Security Headers | Low/Medium | Fixed |
| SEC-004 | Missing Rate Limiting | Medium | Fixed |

### Summary

The assessment identified four primary security areas requiring attention:

- **SEC-001 — BOLA/IDOR:** Object-level authorization was implemented and verified.
- **SEC-002 — SQL Injection:** A controlled SQL Injection vulnerability was identified, remediated using parameterized queries, and successfully retested.
- **SEC-003 — Missing Security Headers:** Recommended HTTP security headers were implemented and verified.
- **SEC-004 — Missing Rate Limiting:** Login requests were rate-limited and the control was verified using HTTP `429 Too Many Requests`.

The detailed technical findings are documented in the following section.

# 5. Detailed Findings

## SEC-001 — Broken Object Level Authorization (BOLA/IDOR)

### Severity

**High**

### Affected Endpoint

```text
GET /api/users/<id>
```

### Description

Broken Object Level Authorization (BOLA), also commonly associated with IDOR, occurs when an application does not properly verify whether an authenticated user is authorized to access a specific object.

In this API, user objects are accessed using a user ID supplied through the URL.

The application was tested to verify whether an authenticated user could request another user's object.

### Security Test

An authenticated user associated with user ID `1` attempted to access another user object:

```text
GET /api/users/2
```

The request was made using a valid JWT belonging to user ID `1`.

### Expected Security Behavior

The application should verify that the authenticated user is authorized to access the requested object.

A user should not be able to access another user's information simply by changing the object ID in the URL.

### Authorization Control

The application implements an object-level authorization check.

The authenticated user ID from the JWT is compared with the requested user ID.

Conceptually, the authorization logic is:

```python
if decoded_token["user_id"] != user_id:
    return {"error": "Access denied"}, 403
```

### Retest Result

After implementing the authorization control, the same request:

```text
GET /api/users/2
```

returned:

```text
403 Forbidden
```

with the following response:

```json
{
    "error": "Access denied"
}
```

### Security Verification

The response confirms that the application does not allow the authenticated user to access another user's object when the requested object ID does not match the authenticated user's ID.

### Remediation

Object-level authorization was implemented so that every protected user-object request is checked against the identity contained in the JWT.

### Security Impact

Without proper object-level authorization, an attacker who knows or guesses another user's object ID may attempt to access information belonging to that user.

This type of weakness can result in unauthorized disclosure or modification of application data.

---

## SEC-002 — SQL Injection

### Severity

**High**

### Affected Endpoint

```text
GET /api/search
```

### Description

SQL Injection occurs when untrusted user input is directly incorporated into an SQL query without proper parameterization or validation.

The `/api/search` endpoint was tested because it accepts user-controlled input through the `name` query parameter.

### Initial Vulnerable Implementation

The endpoint initially constructed the SQL statement by directly concatenating the user-supplied value into the query.

The vulnerable logic was:

```python
query = "SELECT id, name, email FROM users WHERE name = '" + name + "'"
```

This allowed the supplied input to become part of the SQL command itself.

### Normal Security Test

A normal request was first tested:

```text
GET /api/search?name=Pranay
```

The application returned the matching user record.

This established the expected behavior of the endpoint.

### SQL Injection Test

A controlled SQL Injection payload was then supplied:

```text
' OR '1'='1
```

The resulting request was:

```text
GET /api/search?name=' OR '1'='1
```

### Initial Result

The application returned multiple user records instead of only the requested matching user.

This demonstrated that the supplied input was able to influence the logic of the SQL query.

### Root Cause

The root cause was direct concatenation of user-controlled input into an SQL statement.

The application was effectively constructing SQL using untrusted input:

```text
User Input
     |
     v
SQL Query Construction
     |
     v
Database
```

Because the input was inserted directly into the SQL statement, special SQL characters could alter the intended query logic.

### Remediation

The vulnerable SQL query was replaced with a parameterized query.

The corrected implementation is:

```python
query = "SELECT id, name, email FROM users WHERE name = ?"

users = connection.execute(query, (name,)).fetchall()
```

With parameterized queries, the user's input is treated as data rather than executable SQL syntax.

### Retest

The same SQL Injection payload was tested again:

```text
' OR '1'='1
```

The application returned:

```text
[]
```

### Retest Result

The SQL Injection payload no longer altered the database query logic.

The endpoint correctly treated the supplied value as a search string.

### Security Verification

The SQL Injection vulnerability was successfully remediated and verified through retesting.

### Security Impact

SQL Injection can allow attackers to manipulate database queries.

Depending on the application's database permissions and functionality, SQL Injection may lead to:

- Unauthorized data access
- Data modification
- Data deletion
- Authentication bypass
- Database information disclosure

### Recommendation

Use parameterized queries or prepared statements for all database operations involving user-controlled input.

User input should never be directly concatenated into SQL statements.

## SEC-003 — Missing Security Headers

### Severity

**Low/Medium**

### Description

HTTP security headers provide additional protection against common web-based attacks and browser-related security risks.

During the initial assessment, the API responses did not include several recommended security headers.

The initial response headers included standard headers such as:

```text
Content-Type
Content-Length
Connection
Server
```

However, important security-hardening headers were missing.

### Security Test

The API response headers were inspected using Postman.

The following security headers were checked:

```text
X-Content-Type-Options
X-Frame-Options
Content-Security-Policy
```

### Security Weakness

The absence of these headers reduces the application's defense-in-depth protections.

For example:

- Missing `X-Content-Type-Options` may allow browsers to perform MIME-type sniffing.
- Missing `X-Frame-Options` may increase exposure to clickjacking when the application is rendered in a browser.
- Missing `Content-Security-Policy` removes an important browser-side control for restricting content sources.

### Remediation

Security headers were added globally to Flask responses using an `after_request` handler.

The implemented code is:

```python
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

### Retest

After restarting the Flask application, the response headers were inspected again using Postman.

### Retest Result

The following headers were successfully returned:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

### Security Verification

The required security headers were successfully implemented and verified.

### Security Impact

Missing security headers generally represent a hardening weakness rather than a direct application compromise.

However, appropriate security headers provide additional protection against browser-based attacks and reduce the application's overall attack surface.

### Recommendation

Security headers should be reviewed periodically and configured according to the application's deployment requirements.

For production environments, the Content Security Policy should be designed based on the application's actual scripts, styles, APIs, and other required content sources rather than using a generic policy.

---

## SEC-004 — Missing Rate Limiting

### Severity

**Medium**

### Affected Endpoint

```text
POST /api/login
```

### Description

Rate limiting restricts the number of requests that a client can make within a defined period.

Authentication endpoints are particularly important because unrestricted login requests can allow attackers to perform automated password-guessing or brute-force attempts.

### Security Test

Repeated login requests were sent to:

```text
POST /api/login
```

The purpose of the test was to determine whether the application restricted excessive authentication attempts.

### Security Weakness

Without a request-rate control, an attacker could repeatedly submit login requests.

The basic attack pattern could be represented as:

```text
Attacker
   |
   | Repeated Login Requests
   v
/api/login
   |
   v
Authentication System
```

A large number of automated requests could place additional load on the application and increase the feasibility of password-guessing attacks.

### Remediation

Flask-Limiter was integrated into the application.

The login endpoint was configured with the following limit:

```python
@limiter.limit("5 per minute")
```

This configuration restricts a client to five login requests per minute.

### Rate-Limiting Configuration

The Flask-Limiter instance was configured using the client's remote address:

```python
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)
```

### Retest

Multiple login requests were sent repeatedly using Postman.

After the configured limit was exceeded, the API was tested for its response.

### Retest Result

The application returned:

```text
429 Too Many Requests
```

The response indicated the configured limit:

```text
5 per 1 minute
```

### Security Verification

The rate-limiting control successfully restricted excessive authentication requests.

The HTTP `429 Too Many Requests` response confirmed that the configured request limit was being enforced.

### Security Impact

Without rate limiting, attackers may automate large numbers of authentication requests.

Rate limiting helps reduce:

- Brute-force attempts
- Automated password guessing
- Credential-stuffing attempts
- Excessive API requests
- Resource consumption caused by repeated requests

### Recommendation

Authentication endpoints should always implement appropriate rate limiting.

For production systems, rate limits should be selected based on legitimate user behavior and may be combined with additional controls such as:

- Account lockout policies
- Multi-factor authentication
- CAPTCHA or bot detection
- Monitoring and alerting
- IP reputation controls
- Failed-login tracking

Rate limiting should be considered a mitigation control rather than a complete solution to brute-force attacks.

# 6. Authentication and Authorization Controls

## 6.1 JWT Authentication

The SecureAPI application uses JSON Web Tokens (JWT) to authenticate users.

JWT provides a mechanism for securely transmitting authentication information between the client and the API.

### Authentication Flow

```text
User
  |
  | Email + Password
  v
POST /api/login
  |
  | Credentials Verified
  v
JWT Token Generated
  |
  v
Client Stores Token
  |
  | Authorization: Bearer <JWT>
  v
Protected API Endpoint
  |
  v
JWT Verification
  |
  v
Access Granted / Denied
```

### Login Request

The user provides valid credentials to the login endpoint:

```http
POST /api/login
```

Example request:

```json
{
    "email": "pranay@example.com",
    "password": "<YOUR_LOCAL_TEST_PASSWORD>"
}
```

### Successful Authentication

If the credentials are valid, the application generates a JWT.

The client can then use the token when accessing protected endpoints.

The token is sent using the HTTP Authorization header:

```text
Authorization: Bearer <JWT_TOKEN>
```

### Authentication Failure

If a request to a protected endpoint does not contain a valid JWT, the API denies the request.

Typical authentication failures result in:

```text
401 Unauthorized
```

---

## 6.2 Password Security

User passwords are not stored directly as plain text.

The application uses password hashing through Werkzeug's password hashing functionality.

Conceptually, the process is:

```text
User Password
      |
      v
Password Hashing
      |
      v
Stored Password Hash
```

During login:

```text
Entered Password
      |
      v
Password Verification
      |
      v
Stored Password Hash
      |
      v
Match / No Match
```

### Why Hashing Is Used

Password hashing protects stored passwords from being directly exposed if the database is accessed.

Hashing is different from encryption because a properly designed password hash is not intended to be reversed back into the original password.

---

## 6.3 Authorization

Authentication answers:

```text
WHO are you?
```

Authorization answers:

```text
WHAT are you allowed to access?
```

A user can be successfully authenticated but still be unauthorized to access a particular resource.

### Example

Suppose:

```text
User ID = 1
```

attempts to access:

```text
/api/users/2
```

The API must verify whether user ID 1 is authorized to access user ID 2.

The application performs this object-level authorization check before returning the requested user information.

---

## 6.4 Authentication vs Authorization

| Security Concept | Purpose | Example |
|---|---|---|
| Authentication | Verifies identity | Login using email and password |
| Authorization | Verifies permissions | Checking whether user 1 can access user 2 |
| JWT | Carries authenticated identity information | Bearer token |
| Password Hashing | Protects stored passwords | Werkzeug password hash |

---

## 6.5 HTTP Status Codes Used

The API uses HTTP status codes to communicate authentication and authorization results.

### 200 OK

The request was successfully processed.

```text
200 OK
```

### 401 Unauthorized

The request does not contain valid authentication credentials.

```text
401 Unauthorized
```

Example:

```text
Missing or invalid JWT
```

### 403 Forbidden

The user is authenticated but does not have permission to access the requested resource.

```text
403 Forbidden
```

Example:

```text
Authenticated user attempts to access another user's object
```

### 429 Too Many Requests

The client has exceeded the configured request-rate limit.

```text
429 Too Many Requests
```

Example:

```text
More than 5 login requests within the configured time period
```

---

## 6.6 Protected API Request

A protected request follows this structure:

```http
GET /api/users/1
Authorization: Bearer <JWT_TOKEN>
```

The API performs the following sequence:

```text
Request Received
      |
      v
Authorization Header Checked
      |
      v
JWT Extracted
      |
      v
JWT Verified
      |
      v
User Identity Determined
      |
      v
Authorization Check
      |
      v
Resource Returned
```

If any required security check fails, the request is rejected.

---

## 6.7 Security Controls Implemented

The authentication and authorization layer contains the following controls:

- Password hashing
- JWT-based authentication
- Protected API endpoints
- Bearer token authentication
- JWT validation
- Object-level authorization
- HTTP status-code based access control
- Rate limiting on the login endpoint

These controls provide multiple layers of protection around the API's authentication and authorization mechanisms.

# 7. Security Controls Implemented

The SecureAPI application was progressively hardened by implementing multiple security controls.

These controls address authentication, authorization, database security, HTTP security, and API abuse.

---

## 7.1 Password Hashing

Passwords are stored using secure password hashing rather than plain-text storage.

### Control

```text
Plain Password
      |
      v
Password Hashing
      |
      v
Password Hash Stored in Database
```

### Security Benefit

If the database is exposed, attackers do not immediately obtain the original plain-text passwords.

---

## 7.2 JWT Authentication

JWT-based authentication was implemented for protected API endpoints.

### Control

```text
Email + Password
      |
      v
Credential Verification
      |
      v
JWT Generated
      |
      v
Bearer Token
      |
      v
Protected Endpoint
```

### Security Benefit

Only requests containing a valid authentication token can access protected resources.

---

## 7.3 Object-Level Authorization

Object-level authorization was implemented for user resources.

### Control

The authenticated user's ID is compared with the requested object ID.

```text
JWT User ID
     |
     v
Authorization Check
     |
     +------ Match ------> Access Allowed
     |
     +------ No Match --> 403 Forbidden
```

### Security Benefit

This prevents authenticated users from accessing user objects that they are not authorized to access.

---

## 7.4 SQL Injection Protection

The application was initially tested for SQL Injection.

The vulnerable query used direct string concatenation.

The application was remediated using parameterized SQL queries.

### Secure Implementation

```python
query = "SELECT id, name, email FROM users WHERE name = ?"

users = connection.execute(query, (name,)).fetchall()
```

### Security Benefit

The database treats user input as data instead of executable SQL syntax.

---

## 7.5 HTTP Security Headers

The following security headers were implemented:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

### Security Benefit

These headers provide additional browser-side security protections and improve the application's defense-in-depth posture.

---

## 7.6 API Rate Limiting

Rate limiting was implemented on the login endpoint.

### Configuration

```python
@limiter.limit("5 per minute")
```

### Security Benefit

The control restricts excessive authentication requests and helps reduce automated password-guessing and brute-force attempts.

When the configured limit is exceeded, the application returns:

```text
429 Too Many Requests
```

---

## 7.7 Authentication-Protected Endpoints

Protected endpoints require a valid JWT before processing authenticated requests.

### Request Structure

```http
GET /api/users/1
Authorization: Bearer <JWT_TOKEN>
```

### Security Flow

```text
API Request
     |
     v
JWT Present?
     |
     +---- No ----> 401 Unauthorized
     |
     v
JWT Valid?
     |
     +---- No ----> 401 Unauthorized
     |
     v
Authorization Check
     |
     +---- Fail ---> 403 Forbidden
     |
     v
Resource Access
```

---

## 7.8 Security Testing Using Postman

Postman was used to manually test the application's security controls.

The following tests were performed:

| Test | Purpose | Result |
|---|---|---|
| Login testing | Verify authentication | Successful |
| JWT testing | Verify protected endpoints | Successful |
| Authorization testing | Verify object-level access control | 403 returned |
| SQL Injection testing | Test database input handling | Remediated |
| Header inspection | Verify security headers | Headers present |
| Rate-limit testing | Test excessive requests | 429 returned |

---

## 7.9 Overall Security Control Architecture

The implemented controls can be represented as:

```text
                    SecureAPI
                       |
        +--------------+--------------+
        |              |              |
 Authentication   Authorization   Input Security
        |              |              |
       JWT          BOLA/IDOR       SQLi Protection
        |              |              |
        +--------------+--------------+
                       |
                API Hardening
                       |
             +---------+---------+
             |                   |
       Security Headers     Rate Limiting
             |                   |
             +---------+---------+
                       |
                       v
                Protected API
```

The combination of these controls provides layered protection across the application's authentication, authorization, database, HTTP, and API-abuse surfaces.

# 8. Testing Evidence

This section documents the security tests performed against SecureAPI and the results obtained after implementing the corresponding security controls.

---

## 8.1 BOLA / IDOR Testing

### Objective

Verify that an authenticated user cannot access another user's object without authorization.

### Test Configuration

```text
Authenticated User ID: 1
Requested User ID: 2
```

### Test Request

```http
GET /api/users/2
```

The request was sent using a valid JWT belonging to user ID `1`.

### Expected Result

The API should deny access because the authenticated user is not authorized to access the requested object.

### Actual Result

```text
HTTP/1.1 403 Forbidden
```

Response:

```json
{
    "error": "Access denied"
}
```

### Conclusion

The object-level authorization control successfully prevented unauthorized access to the requested user object.

---

## 8.2 SQL Injection Testing

### Objective

Determine whether user-controlled input can alter the logic of an SQL query.

### Affected Endpoint

```http
GET /api/search
```

### Normal Request

```text
GET /api/search?name=Pranay
```

### Normal Behavior

The API returned the matching user record.

### Injection Payload

```text
' OR '1'='1
```

### Injection Request

```text
GET /api/search?name=' OR '1'='1
```

### Initial Behavior

Before remediation, the input altered the SQL query logic and caused multiple user records to be returned.

This confirmed that the endpoint was vulnerable to SQL Injection.

### Remediation

The SQL query was changed from direct string concatenation to a parameterized query.

### Secure Query

```python
query = "SELECT id, name, email FROM users WHERE name = ?"

users = connection.execute(query, (name,)).fetchall()
```

### Retest

The same payload was submitted after remediation:

```text
' OR '1'='1
```

### Retest Result

```text
[]
```

### Conclusion

The SQL Injection vulnerability was successfully remediated.

The same input was treated as a search value rather than SQL syntax.

---

## 8.3 HTTP Security Header Testing

### Objective

Verify whether recommended HTTP security headers are present in API responses.

### Headers Tested

```text
X-Content-Type-Options
X-Frame-Options
Content-Security-Policy
```

### Initial Assessment

The application initially did not return these security-hardening headers.

### Remediation

The following headers were added:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

### Retest Result

The headers were confirmed in the HTTP response.

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

### Conclusion

The recommended security headers were successfully implemented and verified.

---

## 8.4 Rate-Limiting Testing

### Objective

Determine whether repeated authentication requests are restricted.

### Affected Endpoint

```http
POST /api/login
```

### Configured Limit

```text
5 requests per minute
```

### Test Method

Multiple login requests were repeatedly sent using Postman.

### Expected Behavior

After the configured limit was reached, additional requests should be rejected.

### Retest Result

The application returned:

```text
HTTP/1.1 429 Too Many Requests
```

The response indicated:

```text
5 per 1 minute
```

### Conclusion

The configured rate limit was successfully enforced.

---

## 8.5 Authentication Testing

### Objective

Verify that protected API endpoints require valid authentication.

### Test Case 1 — Valid JWT

A valid JWT was supplied with the request.

```http
Authorization: Bearer <VALID_JWT>
```

### Result

The authenticated request was processed successfully when the user was authorized to access the requested resource.

```text
200 OK
```

---

### Test Case 2 — Missing JWT

A protected endpoint was accessed without an authentication token.

```http
GET /api/users/1
```

without:

```http
Authorization: Bearer <JWT>
```

### Expected Result

The API should reject the request because authentication credentials are missing.

```text
401 Unauthorized
```

---

### Test Case 3 — Invalid JWT

A request containing an invalid or malformed JWT should also be rejected.

### Expected Result

```text
401 Unauthorized
```

### Conclusion

The authentication layer ensures that protected resources require valid authentication credentials.

---

## 8.6 HTTP Status Code Verification

The security testing process verified the use of appropriate HTTP status codes.

| Status Code | Meaning | Security Scenario |
|---|---|---|
| 200 | OK | Valid authorized request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but unauthorized |
| 429 | Too Many Requests | Rate limit exceeded |

These status codes provide useful information to API clients while clearly representing the result of security checks.

---

## 8.7 Testing Summary

The final testing results can be summarized as follows:

| Security Test | Expected Security Control | Result |
|---|---|---|
| JWT Authentication | Valid token required | Passed |
| BOLA/IDOR | Unauthorized object access denied | Passed |
| SQL Injection | Input treated as data | Passed |
| Security Headers | Required headers present | Passed |
| Rate Limiting | Excessive requests restricted | Passed |

All implemented security controls were re-tested after remediation.

```text
Vulnerability Identification
          |
          v
       Remediation
          |
          v
        Retest
          |
          v
    Security Verified
```

# 9. Tools Used

The following tools and technologies were used during the development and security assessment of SecureAPI.

| Tool / Technology | Purpose |
|---|---|
| Python | Application development and security implementation |
| Flask | REST API development |
| SQLite | Local database |
| JWT | Authentication |
| Werkzeug | Password hashing and verification |
| Flask-Limiter | API rate limiting |
| Postman | API testing and security testing |
| Visual Studio Code | Development and code analysis |
| Git | Version control |
| GitHub | Source-code management and project documentation |

---

## 9.1 Python

Python was used as the primary programming language for developing the API.

It was used to implement:

- API endpoints
- Authentication
- Authorization
- Database interaction
- Security controls
- Vulnerability remediation

---

## 9.2 Flask

Flask was used as the web framework for developing the REST API.

The framework provided functionality for:

- Routing
- HTTP request handling
- JSON responses
- Middleware
- API endpoint development
- Response security headers

---

## 9.3 SQLite

SQLite was used as the local database.

The database stores sample user information and is accessed through Python.

The architecture is:

```text
Client
  |
  v
Flask API
  |
  v
Python Database Layer
  |
  v
SQLite Database
```

---

## 9.4 JWT

JSON Web Tokens were used to implement authentication.

JWT allows the API to identify an authenticated user when accessing protected endpoints.

The token is supplied through:

```http
Authorization: Bearer <JWT_TOKEN>
```

---

## 9.5 Flask-Limiter

Flask-Limiter was used to implement API rate limiting.

The login endpoint was configured with:

```python
@limiter.limit("5 per minute")
```

This helped mitigate excessive authentication requests.

---

## 9.6 Postman

Postman was used as the primary API testing tool.

It was used to:

- Send GET requests
- Send POST requests
- Test login
- Obtain JWT tokens
- Send Bearer tokens
- Test authorization
- Test SQL Injection
- Inspect HTTP headers
- Test rate limiting
- Verify HTTP status codes

---

## 9.7 Visual Studio Code

Visual Studio Code was used for:

- Writing Python code
- Modifying security controls
- Debugging the API
- Reviewing source code
- Creating the VAPT report
- Managing project files

---

# 10. Key Security Concepts Demonstrated

The SecureAPI project demonstrates practical understanding of several application-security concepts.

---

## 10.1 Vulnerability Assessment and Penetration Testing

Vulnerability Assessment and Penetration Testing (VAPT) is a structured process used to identify, validate, assess, and remediate security weaknesses.

The project followed this basic lifecycle:

```text
Reconnaissance
      |
      v
Testing
      |
      v
Vulnerability Identification
      |
      v
Risk Assessment
      |
      v
Remediation
      |
      v
Retesting
      |
      v
Reporting
```

---

## 10.2 Authentication

Authentication verifies the identity of a user.

In simple terms:

```text
Authentication = WHO are you?
```

Example:

```text
Email + Password
       |
       v
Identity Verification
       |
       v
JWT Token
```

---

## 10.3 Authorization

Authorization determines what an authenticated user is allowed to access.

In simple terms:

```text
Authorization = WHAT are you allowed to access?
```

Example:

```text
User 1
  |
  v
Request User 2's Data
  |
  v
Authorization Check
  |
  v
403 Forbidden
```

---

## 10.4 BOLA / IDOR

Broken Object Level Authorization occurs when an application fails to verify whether a user is authorized to access a specific object.

For example:

```text
GET /api/users/2
```

A user authenticated as user `1` should not automatically receive user `2`'s information.

The application must perform an authorization check.

---

## 10.5 SQL Injection

SQL Injection occurs when an attacker can manipulate an application's SQL query through malicious input.

Unsafe approach:

```python
query = "SELECT * FROM users WHERE name = '" + name + "'"
```

Safer approach:

```python
query = "SELECT * FROM users WHERE name = ?"
```

Parameterized queries separate SQL commands from user-controlled data.

---

## 10.6 Security Headers

HTTP security headers provide additional protection against certain browser-based attacks.

The project implemented:

```text
X-Content-Type-Options
X-Frame-Options
Content-Security-Policy
```

These controls improve the application's defense-in-depth security posture.

---

## 10.7 Rate Limiting

Rate limiting controls how frequently a client can send requests.

Example:

```text
5 login requests
      |
      v
Within 1 minute
      |
      v
Additional request
      |
      v
429 Too Many Requests
```

Rate limiting helps reduce automated abuse and brute-force attempts.

---

## 10.8 Vulnerability Remediation

Finding vulnerabilities is only one part of security testing.

A complete security workflow should also include remediation and retesting.

```text
Find Vulnerability
        |
        v
Understand Root Cause
        |
        v
Implement Fix
        |
        v
Retest
        |
        v
Verify Fix
```

This project followed that process for the identified security weaknesses.

---

# 11. Conclusion

The SecureAPI project demonstrates a practical application-security testing workflow against a locally hosted Flask REST API.

The project covered multiple areas of application security, including:

- Authentication
- Authorization
- JWT
- Password hashing
- BOLA / IDOR
- SQL Injection
- Parameterized SQL queries
- HTTP security headers
- API rate limiting
- Security testing
- Vulnerability remediation
- Retesting
- Technical security documentation

The project was designed around a controlled environment where vulnerabilities could be safely introduced, tested, fixed, and verified.

The overall security assessment lifecycle was:

```text
                    SecureAPI
                       |
                       v
                Reconnaissance
                       |
                       v
              Endpoint Identification
                       |
                       v
              Security Testing
                       |
          +------------+------------+
          |            |            |
          v            v            v
        Auth         SQLi       API Security
          |            |            |
          +------------+------------+
                       |
                       v
             Vulnerability Analysis
                       |
                       v
                  Remediation
                       |
                       v
                    Retesting
                       |
                       v
              Security Verification
                       |
                       v
                VAPT Reporting
```

The assessment demonstrates the importance of identifying vulnerabilities, understanding their root causes, implementing appropriate security controls, and validating the fixes through retesting.

This project provides practical exposure to the fundamental workflow used in application-security and VAPT activities.

# 12. Final Assessment Summary

The SecureAPI security assessment demonstrated the practical process of identifying, testing, remediating, and retesting common application-security weaknesses.

The assessment focused on security controls around:

- Authentication
- Authorization
- Database security
- API security
- HTTP security
- Abuse prevention

The final application includes multiple security controls designed to reduce common attack risks.

---

## 12.1 Final Security Status

| Security Area | Control | Status |
|---|---|---|
| Authentication | JWT authentication | Implemented |
| Password Security | Password hashing | Implemented |
| Authorization | Object-level authorization | Implemented |
| BOLA/IDOR | Authorization validation | Fixed and verified |
| SQL Injection | Parameterized queries | Fixed and verified |
| HTTP Security | Security headers | Implemented and verified |
| API Abuse | Login rate limiting | Implemented and verified |
| Security Testing | Postman testing | Completed |
| Retesting | Verification after remediation | Completed |
| Documentation | VAPT report | Completed |

---

## 12.2 Overall Assessment

The assessment demonstrates that security testing should not stop after identifying a vulnerability.

A complete security process includes:

```text
Identify
   |
   v
Validate
   |
   v
Understand Root Cause
   |
   v
Remediate
   |
   v
Retest
   |
   v
Document
```

This approach ensures that identified weaknesses are not only reported but also addressed and verified.

---

# 13. Lessons Learned

The project provided practical understanding of the following areas.

### 13.1 Authentication and Authorization

Authentication and authorization are separate security concepts.

```text
Authentication
=
WHO are you?

Authorization
=
WHAT can you access?
```

A valid login does not automatically mean that the user can access every resource in the application.

---

### 13.2 Secure Database Interaction

User input should never be blindly inserted into SQL queries.

Parameterized queries provide a safer method of interacting with databases.

```text
User Input
    |
    v
Parameterized Query
    |
    v
Database
```

---

### 13.3 Defense in Depth

Application security should use multiple layers of protection.

For SecureAPI:

```text
Password Hashing
       +
JWT Authentication
       +
Authorization
       +
SQL Injection Protection
       +
Security Headers
       +
Rate Limiting
       =
Layered Security
```

No single security control should be considered sufficient on its own.

---

### 13.4 Importance of Retesting

A vulnerability should be retested after remediation.

For example:

```text
SQL Injection Found
        |
        v
Parameterized Query Implemented
        |
        v
Same Payload Tested Again
        |
        v
SQL Injection No Longer Effective
```

This provides evidence that the remediation was effective.

---

# 14. Future Security Improvements

Although the project implements several important security controls, a production application would require additional security measures.

Potential future improvements include:

- HTTPS/TLS configuration
- Secure cookie configuration
- Refresh-token management
- JWT expiration and rotation
- Multi-factor authentication
- Account lockout controls
- Strong password policies
- Input validation
- Centralized logging
- Security monitoring
- Audit trails
- CORS configuration
- CSRF protection where applicable
- API gateway protection
- Secrets management
- Dependency vulnerability scanning
- Automated security testing
- Burp Suite testing
- Nmap reconnaissance
- SAST and DAST integration
- CI/CD security checks

These improvements would allow the project to move closer to a production-grade application-security architecture.

---

# 15. Responsible Security Testing

All security testing performed during this project was conducted against a locally hosted application controlled by the developer.

Testing was performed for educational and defensive purposes.

The SQL Injection payloads and authorization tests were executed only against the local SecureAPI environment.

No external production systems or third-party applications were targeted.

---

# 16. Project Security Testing Checklist

The following checklist was used during the assessment.

### Reconnaissance

- [x] Identify application
- [x] Identify API endpoints
- [x] Identify authentication mechanism
- [x] Identify database technology
- [x] Identify security controls

### Authentication

- [x] Test login functionality
- [x] Test valid credentials
- [x] Test protected endpoints
- [x] Test JWT authentication
- [x] Test missing authentication

### Authorization

- [x] Test object-level authorization
- [x] Test cross-user object access
- [x] Verify `403 Forbidden`
- [x] Implement authorization control
- [x] Retest authorization

### Input Security

- [x] Identify user-controlled input
- [x] Test SQL Injection
- [x] Identify vulnerable query construction
- [x] Implement parameterized query
- [x] Retest SQL Injection

### API Hardening

- [x] Inspect HTTP headers
- [x] Implement security headers
- [x] Verify security headers
- [x] Implement rate limiting
- [x] Test excessive requests
- [x] Verify `429 Too Many Requests`

### Reporting

- [x] Document vulnerabilities
- [x] Document severity
- [x] Document affected endpoints
- [x] Document root causes
- [x] Document remediation
- [x] Document retest results
- [x] Document security recommendations

---

# 17. Final Conclusion

SecureAPI provided a controlled environment for understanding the complete application-security testing lifecycle.

The project demonstrated that effective VAPT involves more than simply finding vulnerabilities.

A security professional must be able to:

1. Understand the application's functionality.
2. Identify attack surfaces.
3. Test security controls.
4. Validate vulnerabilities.
5. Understand the root cause.
6. Assess potential impact.
7. Recommend remediation.
8. Implement or verify fixes.
9. Retest the application.
10. Clearly document the results.

The final SecureAPI implementation demonstrates practical knowledge of REST API security, authentication, authorization, SQL Injection prevention, HTTP security hardening, rate limiting, vulnerability remediation, and technical security reporting.

```text
                 SECUREAPI VAPT LIFECYCLE

                       Application
                           |
                           v
                    Reconnaissance
                           |
                           v
                  Attack Surface Mapping
                           |
                           v
                    Security Testing
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
   Authentication    Authorization       SQL/API
       Testing           Testing          Testing
          |                |                |
          +----------------+----------------+
                           |
                           v
                 Vulnerability Analysis
                           |
                           v
                       Remediation
                           |
                           v
                        Retesting
                           |
                           v
                  Security Verification
                           |
                           v
                    Technical Report
```

**End of VAPT Security Assessment Report**