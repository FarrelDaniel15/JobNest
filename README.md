# JobNest 🪺

> A full-stack web application designed to streamline, organize, and track job applications through every stage of the hiring pipeline.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

---

## 📌 Overview

Applying for jobs across multiple boards (LinkedIn, Indeed, company career portals) often leads to fragmented tracking and missed updates. **JobNest** solves this problem by providing job seekers with a centralized personal dashboard to monitor application dates, track statuses across custom recruitment stages, and maintain detailed record histories.

---

## ✨ Key Features

* **🔐 User Authentication:** Secure sign-up, login, and session management using hashed passwords (`werkzeug.security`) and custom session error handling.
* **📊 Analytics Dashboard:** Overview of pending, active, and finalized job applications with real-time status indicators.
* **📝 Full Application CRUD:**
  * **Add:** Log new applications with company name, role, application date, status, and tailored notes.
  * **Edit/Update:** Easily transition applications between stages (e.g., *Applied* → *Interviewing* → *Offer / Rejected*).
  * **Delete:** Remove outdated entries from the database.
* **🎨 Modern UI & Responsive Design:** Sleek interface styled with **Tailwind CSS** alongside custom stylesheets (`styles.css`), utilizing Jinja2 template inheritance (`layout.html`) for modular components and consistent rendering across devices.

---

## 🛠️ Tech Stack & Architecture

### **Backend**
* **Python (Flask):** Handles application routing, request processing, dynamic template rendering, and session management (`app.py`)[cite: 1].
* **SQLite3 (`jobnest.db`):** Relational database storage managing user accounts and application tables[cite: 1].

### **Frontend**
* **HTML5 / Jinja2:** Template layout architecture (`templates/`) for modular code reusability[cite: 1].
* **Tailwind CSS & Custom CSS3:** Utility-first styling with Tailwind CSS complemented by custom styles (`static/styles.css`) for responsive, intuitive UI design[cite: 1].

---

## 📂 Directory Structure

```text
JobNest/
│
├── static/
│   ├── image/
│   │   ├── JobNest_Logo.jpg
│   │   └── JobNest_Small_Logo.jpg
│   └── styles.css       # Tailwind CSS build & custom stylesheets
│
├── templates/
│   ├── add.html         # Application submission form
│   ├── apology.html     # Custom error reporting page
│   ├── dashboard.html   # Main application overview
│   ├── edit.html        # Application editing modal/page
│   ├── index.html       # Landing page
│   ├── layout.html      # Base Jinja template with navigation
│   ├── login.html       # User sign-in interface
│   └── register.html    # User registration page
│
├── app.py               # Main Flask server routing & logic
├── jobnest.db           # SQLite database schema and storage
└── requirements.txt     # Python dependencies