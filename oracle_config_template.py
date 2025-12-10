import cx_Oracle
from sqlalchemy.pool import NullPool


ORACLE_HOST = "prophet.njit.edu"  # NJIT Oracle server
ORACLE_PORT = 1521
ORACLE_SID = "course"      # Your SID
ORACLE_USERNAME = "YOUR_USERNAME_HERE"   # Replace with your schema name
ORACLE_PASSWORD = "YOUR_PASSWORD_HERE"   # Replace with your password

# Build DSN using cx_Oracle.makedsn with SID (tested and working!)
ORACLE_DSN = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, sid=ORACLE_SID)

# Create a connection factory function
def get_oracle_connection():
    """Create and return a new Oracle database connection"""
    return cx_Oracle.connect(
        user=ORACLE_USERNAME,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN,
        encoding="UTF-8"
    )

# For SQLAlchemy, we'll use the creator parameter instead of connection string
# This bypasses URL parsing issues with special characters in password
ORACLE_CONNECTION_STRING = "oracle+cx_oracle://"  # Placeholder
ORACLE_ENGINE_OPTIONS = {
    "creator": get_oracle_connection,
    "poolclass": NullPool  # Disable pooling for simplicity
}
