# Cafe Management System

A web-based Cafe Management System built with **Python, FastAPI, MySQL, HTML, CSS, and JavaScript**. It helps manage cafe operations, including customers, menu items, orders, inventory, reservations, employees, and sales reports.

## Features

- **Customer Management** – Customer registration, login, profile management, and authentication.
- **Authentication & Security** – JWT-based authentication and password hashing.
- **OTP & Password Reset** – OTP-based verification and password reset functionality.
- **Menu Management** – View and manage cafe menu items.
- **Order Management** – Create and manage customer orders.
- **Inventory Management** – Manage ingredients and inventory details.
- **Reservation Management** – Handle customer reservations.
- **Employee Management** – Manage employee information.
- **Loyalty Points** – Track customer loyalty points.
- **Feedback Management** – Collect and manage customer feedback.
- **Sales Reports** – View sales-related reports.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| API Testing | Swagger UI, Postman |

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kathirvelp39/Cafe-Management-System.git
cd Cafe-Management-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If the project includes a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

- Make sure MySQL Server is installed and running.
- Create the required database.
- Configure the database connection using your local MySQL credentials.
- Keep database passwords and secret keys out of GitHub.

### 5. Run the Backend

From the project root, run:

```bash
uvicorn server.main:app --reload
```

The backend API will be available at:

```text
http://127.0.0.1:8000
```

### 6. Access API Documentation

Open the following URL in your browser:

```text
http://127.0.0.1:8000/docs
```

### 7. Run the Frontend

Open `client/index.html` using VS Code Live Server or another local web server.

Make sure the frontend API base URL matches the backend address.

## API Documentation

FastAPI provides interactive API documentation through Swagger UI:

`http://127.0.0.1:8000/docs`

## Security Notes

- Do not commit `.env` files or database credentials.
- Do not upload virtual environments such as `venv/` or `.venv/`.
- Do not upload JWT tokens, passwords, or other secret information.
- Configure your own local database credentials before running the application.

## Author

**Kathirvel P**

---

*This project was developed to simplify and organize cafe management operations through a web-based application.*