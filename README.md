# Flight Booking System - User Management Interface

**CS 331 Database Systems - Group 14**

A Flask-based web application for managing flight bookings, connected to an Oracle database at NJIT.

## Project Component

This repository contains the **User Management Interface** for the Flight Booking Database project, including:
- User authentication (login/register)
- Passenger profile management
- Flight search and booking
- Reservation management

## Setup & Run

1. **Create and activate a virtual environment:**
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   
   # Activate it (macOS/Linux)
   source .venv/bin/activate
   
   # Activate it (Windows)
   .venv\Scripts\activate
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Oracle Database Connection:**
   
   ⚠️ **IMPORTANT:** The repository contains `oracle_config_template.py` as a template. You need to create your own configuration file:
   
   ```bash
   # Copy the template to create your config file
   cp oracle_config_template.py oracle_config.py
   ```
   
   Then edit `oracle_config.py` and add your Oracle database credentials:
   ```python
   ORACLE_USERNAME = "your_username_here"   # Your NJIT Oracle schema name
   ORACLE_PASSWORD = "your_password_here"   # Your Oracle password
   ```
   
   **Note:** `oracle_config.py` is in `.gitignore` and will not be committed to prevent exposing credentials.

4. **Connect to NJIT VPN** (Required to access the database!)

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access:** http://127.0.0.1:5000

7. **Login** with any passenger email:
   - ayo@example.com
   - jwest@example.com  
   - maria@example.com
   - lchen@example.com
   - samir@example.com
   
   (Any password works - authentication temporarily disabled)

## Project Files

- `app.py` - Main Flask application
- `models.py` - Database models (Passenger, Flight, Ticket, etc.)
- `oracle_config_template.py` - Template for Oracle database connection (copy to `oracle_config.py`)
- `oracle_config.py` - Your actual Oracle credentials (not in git, create from template)
- `auth_routes.py` - Login/Register routes
- `user_routes.py` - Search/Book/Reservations routes
- `templates/` - HTML templates

## Database

Oracle Database at prophet.njit.edu:1521 (SID: course, Schema: cib5)

Tables: PASSENGER, FLIGHT, TICKET, AIRLINE, AIRPORT, AIRCRAFT, PAYMENT, STAFF

## Features

✈️ Search flights by route and date  
🎫 Book tickets with seat class selection  
📋 View your reservations  
👤 User profile management
