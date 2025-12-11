from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Flight, Ticket, Passenger, Airport, Airline, Aircraft, Payment
from datetime import datetime
from sqlalchemy import or_, and_

# Create blueprint for user routes
user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
@login_required
def profile():
    """
    User Profile Page
    Displays passenger account information
    """
    return render_template('profile.html', user=current_user)


@user_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    Flight Search Page
    Search for flights in Oracle database
    """
    flights = []
    search_performed = False
    
    if request.method == 'POST':
        search_performed = True
        origin = request.form.get('origin', '').strip().upper()  # Oracle stores airport codes in uppercase
        destination = request.form.get('destination', '').strip().upper()
        date_str = request.form.get('date')
        
        # Build query
        query = Flight.query
        
        # Search by departure airport code or city
        if origin:
            query = query.join(
                Airport, Flight.departure_airport == Airport.airport_code
            ).filter(
                or_(
                    Flight.departure_airport.ilike(f'%{origin}%'),
                    Airport.city.ilike(f'%{origin}%')
                )
            )
        
        # Search by arrival airport code or city
        if destination:
            query = query.join(
                Airport, Flight.arrival_airport == Airport.airport_code,
                isouter=False
            ).filter(
                or_(
                    Flight.arrival_airport.ilike(f'%{destination}%'),
                    Airport.city.ilike(f'%{destination}%')
                )
            )
        
        # Search by date
        if date_str:
            try:
                search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                query = query.filter(db.func.trunc(Flight.departure_time) == search_date)
            except ValueError:
                flash('Invalid date format.', 'danger')
        
        # Filter flights that have available seats
        flights = [f for f in query.all() if f.available_seats > 0]
        
        if not flights and search_performed:
            flash('No flights found matching your criteria.', 'info')
    
    return render_template('search.html', flights=flights, search_performed=search_performed)


@user_bp.route('/results')
@login_required
def results():
    """
    Flight Results Page
    Shows all available flights from Oracle database
    """
    all_flights = Flight.query.all()
    # Filter to show only flights with available seats
    flights = [f for f in all_flights if f.available_seats > 0]
    return render_template('results.html', flights=flights)


@user_bp.route('/reserve/<string:flight_number>', methods=['GET', 'POST'])
@login_required
def reserve(flight_number):
    """
    Flight Reservation Page
    Books a ticket on the selected flight
    """
    flight = Flight.query.get_or_404(flight_number)
    
    if request.method == 'POST':
        num_passengers = int(request.form.get('num_passengers', 1))
        seat_class = request.form.get('seat_class', 'ECONOMY')  # ECONOMY, BUSINESS, FIRST
        
        # Validation
        if num_passengers < 1:
            flash('Number of passengers must be at least 1.', 'danger')
            return render_template('reserve.html', flight=flight)
        
        if num_passengers > flight.available_seats:
            flash(f'Only {flight.available_seats} seats available.', 'danger')
            return render_template('reserve.html', flight=flight)
        
        # Calculate price based on class
        base_price = 200.0  # You can adjust this or get from aircraft/flight
        if seat_class == 'BUSINESS':
            base_price *= 2.5
        elif seat_class == 'FIRST':
            base_price *= 4.0
        
        total_cost = base_price * num_passengers
        
        # Create tickets for each passenger
        try:
            for i in range(num_passengers):
                # Generate seat number (simplified - you might want more complex logic)
                row = (len(flight.tickets) + i + 1)
                seat_letter = chr(65 + (i % 6))  # A, B, C, D, E, F
                seat_number = f"{row:02d}{seat_letter}"
                
                # Create ticket
                ticket = Ticket(
                    passenger_id=current_user.passenger_id,
                    flight_number=flight.flight_number,
                    seat_number=seat_number,
                    seat_class=seat_class,
                    price=base_price,
                    booking_date=datetime.now(),
                    status='ACTIVE'
                )
                db.session.add(ticket)
            
            db.session.commit()
            flash(f'Flight booked successfully! {num_passengers} ticket(s) created. Total: ${total_cost:.2f}', 'success')
            return redirect(url_for('user.my_reservations'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while booking the flight. Please try again.', 'danger')
            print(f"Reservation error: {e}")
    
    return render_template('reserve.html', flight=flight)


@user_bp.route('/my-reservations')
@login_required
def my_reservations():
    """
    My Tickets/Reservations Page
    Displays all tickets for the current passenger
    """
    tickets = Ticket.query.filter_by(passenger_id=current_user.passenger_id).order_by(Ticket.booking_date.desc()).all()
    return render_template('my_reservations.html', tickets=tickets)


@user_bp.route('/cancel-ticket/<int:ticket_number>', methods=['POST'])
@login_required
def cancel_ticket(ticket_number):
    """
    Cancel Ticket
    Changes ticket status to CANCELED
    """
    ticket = Ticket.query.get_or_404(ticket_number)
    
    # Verify ownership
    if ticket.passenger_id != current_user.passenger_id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('user.my_reservations'))
    
    # Check if already cancelled
    if ticket.status == 'CANCELED':
        flash('This ticket is already cancelled.', 'info')
        return redirect(url_for('user.my_reservations'))
    
    # Update ticket status
    ticket.status = 'CANCELED'
    
    try:
        db.session.commit()
        flash('Ticket cancelled successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while cancelling the ticket.', 'danger')
        print(f"Cancellation error: {e}")
    
    return redirect(url_for('user.my_reservations'))
