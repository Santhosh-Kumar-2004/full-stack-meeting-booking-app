# Role-Based Access Control (RBAC) in FastAPI

## 🧩 Overview

RBAC (Role-Based Access Control) is a security mechanism that restricts access to resources based on a user's role within the system.  
In this FastAPI project, RBAC is implemented to separate normal users from administrators — only admins can perform certain privileged actions such as viewing all registered users.

---

## ⚙️ How RBAC Works in This Project

### 1. **Role Assignment on Registration**
When a user registers via `/auth/register`:
- The backend checks if their email exists in the `.env` variable `ADMIN_EMAILS`.
- If yes → the user is automatically assigned the role **"admin"**.
- Otherwise → the user gets the default role **"user"**.

**Code snippet (from `users.py`):**
```python
role = "admin" if user.email in ADMIN_EMAILS else "user"
```

This ensures that admin rights are not hardcoded but are instead controlled externally via environment variables — improving flexibility and security.

---

### 2. **JWT Token Role Embedding**
During login, a JWT token is created using:
```python
access_token = create_access_token(data={
    "sub": db_user.email,
    "name": db_user.name,
    "role": db_user.role
})
```
This token carries the user's identity and role.  
Frontend stores it in `localStorage` and attaches it in the header when calling protected endpoints.

---

### 3. **Authorization Check (Backend)**
Every protected route uses the dependency `get_current_user`, which:
- Verifies the JWT token.
- Extracts the user info.
- Fetches the user from the database.

Then, specific routes (like `/auth/`) check for admin privileges:
```python
if current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Operation not permitted")
```
This ensures **only admins** can access such endpoints.

---

## 🧠 Mistakes Encountered and Fixes

### ❌ Mistake 1: Admin Email Not Recognized
**Issue:** Newly added admin emails in `.env` were not granting admin privileges.  
**Root Cause:** FastAPI doesn’t automatically reload `.env` values — the backend used an outdated in-memory value.  
**Fix:** Restarted the FastAPI server after updating `.env`.

> ✅ Tip: Always restart your backend after modifying environment variables.

---

### ❌ Mistake 2: Old Admin User Stayed as “User”
**Issue:** A user registered before `.env` was updated kept the `role="user"` even after changes.  
**Fix:** Deleted that user record manually from the database and re-registered after restart.

> ✅ Tip: Role assignment happens only **during registration**, not after.  
> To change roles later, it must be done manually via the database or an admin route.

---

### ❌ Mistake 3: Token Not Updating on Login
**Issue:** When logging in as a new user, the token in `localStorage` was not being updated.  
**Root Cause:** The frontend didn’t overwrite the previous token properly.  
**Fix:** Updated `Login.jsx` to explicitly call:
```js
localStorage.setItem("token", access_token);
```
Now, each login replaces the old token with the latest valid one.

---

## 💡 Real-World RBAC Flow

Here’s how RBAC typically works in a professional system:

1. **User Authentication:**
   - User logs in using credentials.
   - A JWT is issued containing their `role` and other claims.

2. **Access Token Validation:**
   - Every request to a protected endpoint sends the token in the `Authorization` header.

3. **Role Enforcement:**
   - Backend checks the `role` claim in the token or from DB.
   - Grants or denies access based on the required permission.

4. **Example Roles in a Real App:**
   - `admin`: Full access — manage users, view all data, configure system.
   - `manager`: Can manage specific groups or teams.
   - `user`: Basic privileges — can only manage personal data.
   - `guest`: Read-only or temporary access.

5. **Best Practice:**
   - Avoid hardcoding roles in logic — define permissions in config or database.
   - Regularly review admin assignments.
   - Ensure token expiration and revocation policies.

---

## 🧭 Summary of Lessons Learned

| Concept | Mistake | Fix | Key Takeaway |
|----------|----------|-----|--------------|
| Environment Variables | Forgot to restart backend after `.env` changes | Restart FastAPI server | Always reload the backend after changing `.env` |
| Role Assignment | User role not updating | Delete old user and re-register | Role assigned only once during registration |
| Token Handling | Old token remained active | Replaced token on login | Always overwrite the old token on successful login |

---

## 🚀 Conclusion

RBAC provides a structured, secure way to control access in applications.  
By using environment-based admin assignment, JWT-based authentication, and backend route checks, this project achieves a clean, real-world RBAC setup suitable for modern web apps.

