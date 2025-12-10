# Flight Booking System

A Flask web application for managing flight bookings, connected to an Oracle database at NJIT.

## Setup & Run

1. **Connect to NJIT VPN** (Required!)

2. **Run the application:**
   ```bash
   python3.13 app.py
   ```

3. **Access:** http://127.0.0.1:5000

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
