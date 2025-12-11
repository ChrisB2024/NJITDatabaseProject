from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Airport(db.Model):
    """Maps to Airport table in Oracle"""
    __tablename__ = 'AIRPORT'
    
    airport_code = db.Column('AIRPORT_CODE', db.String(8), primary_key=True)
    city = db.Column('CITY', db.String(80), nullable=False)
    country = db.Column('COUNTRY', db.String(80), nullable=False)
    
    def __repr__(self):
        return f'<Airport {self.airport_code} - {self.city}>'


class Airline(db.Model):
    """Maps to Airline table in Oracle"""
    __tablename__ = 'AIRLINE'
    
    airline_id = db.Column('AIRLINE_ID', db.Integer, primary_key=True)
    name = db.Column('NAME', db.String(120), nullable=False, unique=True)
    
    # Relationships
    aircraft = db.relationship('Aircraft', backref='airline', lazy=True)
    flights = db.relationship('Flight', backref='airline', lazy=True)
    staff = db.relationship('Staff', backref='airline', lazy=True)
    
    def __repr__(self):
        return f'<Airline {self.name}>'


class Aircraft(db.Model):
    """Maps to Aircraft table in Oracle"""
    __tablename__ = 'AIRCRAFT'
    
    aircraft_id = db.Column('AIRCRAFT_ID', db.Integer, primary_key=True)
    model = db.Column('MODEL', db.String(80), nullable=False)
    capacity = db.Column('CAPACITY', db.Integer, nullable=False)
    airline_id = db.Column('AIRLINE_ID', db.Integer, db.ForeignKey('AIRLINE.AIRLINE_ID'), nullable=False)
    
    def __repr__(self):
        return f'<Aircraft {self.model}>'


class Flight(db.Model):
    """Maps to Flight table in Oracle"""
    __tablename__ = 'FLIGHT'
    
    flight_number = db.Column('FLIGHT_NUMBER', db.String(10), primary_key=True)
    airline_id = db.Column('AIRLINE_ID', db.Integer, db.ForeignKey('AIRLINE.AIRLINE_ID'), nullable=False)
    aircraft_id = db.Column('AIRCRAFT_ID', db.Integer, db.ForeignKey('AIRCRAFT.AIRCRAFT_ID'), nullable=False)
    departure_airport = db.Column('DEPARTURE_AIRPORT', db.String(8), db.ForeignKey('AIRPORT.AIRPORT_CODE'), nullable=False)
    arrival_airport = db.Column('ARRIVAL_AIRPORT', db.String(8), db.ForeignKey('AIRPORT.AIRPORT_CODE'), nullable=False)
    departure_time = db.Column('DEPARTURE_TIME', db.DateTime, nullable=False)
    arrival_time = db.Column('ARRIVAL_TIME', db.DateTime, nullable=False)
    duration_minutes = db.Column('DURATION_MINUTES', db.Integer)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='flight', lazy=True)
    aircraft_rel = db.relationship('Aircraft', backref='flights', lazy=True)
    dep_airport = db.relationship('Airport', foreign_keys=[departure_airport], backref='departing_flights')
    arr_airport = db.relationship('Airport', foreign_keys=[arrival_airport], backref='arriving_flights')
    
    def __repr__(self):
        return f'<Flight {self.flight_number} - {self.departure_airport} to {self.arrival_airport}>'
    
    @property
    def available_seats(self):
        """Calculate available seats based on aircraft capacity and booked tickets"""
        if self.aircraft_rel:
            booked = len([t for t in self.tickets if t.status == 'ACTIVE'])
            return self.aircraft_rel.capacity - booked
        return 0
    
    @property
    def price(self):
        """Base price for the flight (you can customize this logic)"""
        # Simple pricing: base price of $200
        # You could make this more sophisticated based on distance, demand, etc.
        return 200.00
    
    @property
    def origin(self):
        """Alias for departure_airport for template compatibility"""
        return self.departure_airport
    
    @property
    def destination(self):
        """Alias for arrival_airport for template compatibility"""
        return self.arrival_airport
    
    @property
    def id(self):
        """Return flight_number as id for template compatibility"""
        return self.flight_number


class Passenger(UserMixin, db.Model):
    """
    Maps to Passenger table in Oracle
    Also serves as User for Flask-Login authentication
    """
    __tablename__ = 'PASSENGER'
    
    passenger_id = db.Column('PASSENGER_ID', db.Integer, primary_key=True)
    full_name = db.Column('FULL_NAME', db.String(120), nullable=False)
    date_of_birth = db.Column('DATE_OF_BIRTH', db.Date, nullable=False)
    nationality = db.Column('NATIONALITY', db.String(80), nullable=False)
    phone = db.Column('PHONE', db.String(32))
    email = db.Column('EMAIL', db.String(120), unique=True)
    
    # Additional fields for authentication (you'll need to add this to Oracle)
    # Commented out until you add the column: ALTER TABLE PASSENGER ADD PASSWORD_HASH VARCHAR2(255);
    # password_hash = db.Column('PASSWORD_HASH', db.String(255), nullable=True, server_default=None)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='passenger', lazy=True)
    
    def get_id(self):
        """Required by Flask-Login"""
        return str(self.passenger_id)
    
    def set_password(self, password):
        """Hash and store the password securely"""
        # TODO: Uncomment when PASSWORD_HASH column is added to database
        # self.password_hash = generate_password_hash(password)
        pass
    
    def check_password(self, password):
        """Verify password against stored hash"""
        # TODO: Uncomment when PASSWORD_HASH column is added to database
        # if not self.password_hash:
        #     return False
        # return check_password_hash(self.password_hash, password)
        
        # Temporary: Allow any password for testing
        return True
    
    @property
    def first_name(self):
        """Extract first name from full_name"""
        return self.full_name.split()[0] if self.full_name else ''
    
    @property
    def last_name(self):
        """Extract last name from full_name"""
        parts = self.full_name.split()
        return ' '.join(parts[1:]) if len(parts) > 1 else ''
    
    @property
    def username(self):
        """Use email as username"""
        return self.email
    
    def __repr__(self):
        return f'<Passenger {self.full_name}>'


class Ticket(db.Model):
    """Maps to Ticket table in Oracle"""
    __tablename__ = 'TICKET'
    
    ticket_number = db.Column('TICKET_NUMBER', db.Integer, primary_key=True)
    passenger_id = db.Column('PASSENGER_ID', db.Integer, db.ForeignKey('PASSENGER.PASSENGER_ID'), nullable=False)
    flight_number = db.Column('FLIGHT_NUMBER', db.String(10), db.ForeignKey('FLIGHT.FLIGHT_NUMBER'), nullable=False)
    seat_number = db.Column('SEAT_NUMBER', db.String(6), nullable=False)
    seat_class = db.Column('SEAT_CLASS', db.String(10), nullable=False)  # ECONOMY, BUSINESS, FIRST
    price = db.Column('PRICE', db.Numeric(10, 2), nullable=False)
    booking_date = db.Column('BOOKING_DATE', db.DateTime, nullable=False)
    status = db.Column('STATUS', db.String(12), nullable=False)  # ACTIVE, CANCELED, RESCHEDULED
    
    # Relationships
    payment = db.relationship('Payment', backref='ticket', uselist=False, lazy=True)
    changes = db.relationship('TicketChange', backref='ticket', lazy=True)
    
    def __repr__(self):
        return f'<Ticket {self.ticket_number} - {self.flight_number}>'


class Payment(db.Model):
    """Maps to Payment table in Oracle"""
    __tablename__ = 'PAYMENT'
    
    payment_id = db.Column('PAYMENT_ID', db.Integer, primary_key=True)
    ticket_number = db.Column('TICKET_NUMBER', db.Integer, db.ForeignKey('TICKET.TICKET_NUMBER'), nullable=False, unique=True)
    payment_date = db.Column('PAYMENT_DATE', db.DateTime, nullable=False)
    amount = db.Column('AMOUNT', db.Numeric(10, 2), nullable=False)
    method = db.Column('METHOD', db.String(20), nullable=False)  # CARD, WALLET, CASH
    
    def __repr__(self):
        return f'<Payment {self.payment_id} - ${self.amount}>'


class Staff(db.Model):
    """Maps to Staff table in Oracle"""
    __tablename__ = 'STAFF'
    
    staff_id = db.Column('STAFF_ID', db.Integer, primary_key=True)
    full_name = db.Column('FULL_NAME', db.String(120), nullable=False)
    role = db.Column('ROLE', db.String(40), nullable=False)  # PILOT, COPILOT, CREW
    phone = db.Column('PHONE', db.String(32))
    email = db.Column('EMAIL', db.String(120))
    airline_id = db.Column('AIRLINE_ID', db.Integer, db.ForeignKey('AIRLINE.AIRLINE_ID'), nullable=False)
    
    def __repr__(self):
        return f'<Staff {self.full_name} - {self.role}>'


class FlightStaff(db.Model):
    """Maps to FlightStaff table in Oracle"""
    __tablename__ = 'FLIGHTSTAFF'
    
    flight_number = db.Column('FLIGHT_NUMBER', db.String(10), db.ForeignKey('FLIGHT.FLIGHT_NUMBER'), primary_key=True)
    staff_id = db.Column('STAFF_ID', db.Integer, db.ForeignKey('STAFF.STAFF_ID'), primary_key=True)
    role_on_flight = db.Column('ROLE_ON_FLIGHT', db.String(40), nullable=False)
    
    def __repr__(self):
        return f'<FlightStaff {self.flight_number} - Staff {self.staff_id}>'


class TicketChange(db.Model):
    """Maps to TicketChange table in Oracle"""
    __tablename__ = 'TICKETCHANGE'
    
    change_id = db.Column('CHANGE_ID', db.Integer, primary_key=True)
    ticket_number = db.Column('TICKET_NUMBER', db.Integer, db.ForeignKey('TICKET.TICKET_NUMBER'), nullable=False)
    change_date = db.Column('CHANGE_DATE', db.DateTime, nullable=False)
    new_status = db.Column('NEW_STATUS', db.String(12), nullable=False)
    
    def __repr__(self):
        return f'<TicketChange {self.change_id}>'


# For backward compatibility with existing Flask-Login code
User = Passenger
