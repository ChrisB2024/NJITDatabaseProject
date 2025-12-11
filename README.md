# Flight Booking System

A Fla5. **Access:** http://127.0.0.1:5000

6. **Login** with any passenger email:
   - ayo@example.com
   - jwest@example.com  
   - maria@example.com
   - lchen@example.com
   - samir@example.com
   
   (Any password works - authentication temporarily disabled)lication for managing flight bookings, connected to an Oracle database at NJIT.

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

3. **Connect to NJIT VPN** (Required to access the database!)

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access:** http://127.0.0.1:5000

4. **Login** with any passenger email:
   - ayo@example.com
   - jwest@example.com  
   - maria@example.com
   - lchen@example.com
   - samir@example.com
   
   (Any password works - authentication temporarily disabled)

## Project Files

- `app.py` - Main Flask application
- `models.py` - Database models (Passenger, Flight, Ticket, etc.)
- `oracle_config.py` - Oracle database connection
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
