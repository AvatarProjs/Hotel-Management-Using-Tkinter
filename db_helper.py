import mysql.connector
from mysql.connector import Error, errorcode
from dotenv import load_dotenv
import os
import hashlib
import re
from typing import Optional, Dict, Tuple, List
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self):
        """Initialize database connection with enhanced error handling"""
        self.connection = None
        self._connect()
        self._initialize_database()
        logger.info("DatabaseManager initialized")

    def _connect(self) -> bool:
        """Establish secure connection with retry logic"""
        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                self.connection = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    port=int(os.getenv("DB_PORT")),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME"),
                    ssl_disabled=False,
                    connect_timeout=5,
                    connection_timeout=30,
                    autocommit=True,
                    pool_name="hotel_pool",
                    pool_size=5,
                )

                if self.connection.is_connected():
                    logger.info(f"✅ Connected to MySQL database (Attempt {attempt + 1})")
                    return True

            except Error as err:
                logger.error(f"❌ Connection attempt {attempt + 1} failed: {err}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay)
                    continue
                raise RuntimeError(f"Failed to connect after {max_retries} attempts") from err

    def _initialize_database(self) -> None:
        """Initialize database schema with verification"""
        if not self.connection or not self.connection.is_connected():
            self._connect()

        tables = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL COLLATE utf8mb4_bin,
                    password_hash VARCHAR(255) NOT NULL,
                    gender ENUM('Male','Female','Other') NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            "user_sessions": """
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id VARCHAR(255) PRIMARY KEY,
                    user_id INT NOT NULL,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            "auth_logs": """
                CREATE TABLE IF NOT EXISTS auth_logs (
                    log_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NULL,
                    email VARCHAR(100) NOT NULL,
                    action ENUM('register','login','logout','fail') NOT NULL,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            "reservations": """
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id VARCHAR(20) PRIMARY KEY,
                    user_id INT NOT NULL,
                    guest_name VARCHAR(100) NOT NULL,
                    checkin_date DATE NOT NULL,
                    checkout_date DATE NOT NULL,
                    booking_amount DECIMAL(10,2) NOT NULL,
                    payment_status ENUM('Paid', 'Pending', 'Cancelled') DEFAULT 'Pending',
                    fulfillment_status ENUM('Confirmed', 'Pending', 'Cancelled') DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_reservations_created (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            "customers": """
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id VARCHAR(20) PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL COLLATE utf8mb4_bin,
                    address TEXT NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE INDEX idx_email (email),
                    INDEX idx_status (status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            "transactions": """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id VARCHAR(20),
                    reservation_id VARCHAR(20),
                    amount DECIMAL(10,2) NOT NULL,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
                        ON DELETE SET NULL
                        ON UPDATE CASCADE,
                    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id)
                        ON DELETE SET NULL
                        ON UPDATE CASCADE,
                    INDEX idx_transactions_date (transaction_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            "room_occupancy": """
                CREATE TABLE IF NOT EXISTS room_occupancy (
                    record_id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    occupied_rooms INT NOT NULL,
                    total_rooms INT NOT NULL,
                    UNIQUE KEY unique_date (date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
        }

        try:
            with self.connection.cursor() as cursor:
                # Create all tables with correct definitions
                for table_name, ddl in tables.items():
                    try:
                        cursor.execute(ddl)
                        logger.info(f"Table '{table_name}' created successfully")
                    except Error as err:
                        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                            logger.debug(f"Table '{table_name}' already exists")
                        else:
                            logger.error(f"Error creating table '{table_name}': {err}")
                            raise

            self.connection.commit()
        except Error as err:
            logger.error(f"Database initialization failed: {err}")
            raise

    # ========== DASHBOARD REPORTING METHODS ==========
    def get_total_bookings_cost(self) -> float:
        """Get the total cost of all bookings"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SUM(booking_amount) FROM reservations")
                result = cursor.fetchone()[0]
                return float(result) if result else 0.0
        except Error as err:
            logger.error(f"Error getting total bookings cost: {err}")
            return 0.0

    def get_total_reservations(self) -> int:
        """Get the total number of reservations"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM reservations")
                return cursor.fetchone()[0] or 0
        except Error as err:
            logger.error(f"Error getting total reservations: {err}")
            return 0

    def get_active_customers_count(self) -> int:
        """Get count of active customers"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM customers WHERE status = 'Active'")
                return cursor.fetchone()[0] or 0
        except Error as err:
            logger.error(f"Error getting active customers count: {err}")
            return 0

    def get_total_customers(self) -> int:
        """Get total count of all customers (active and inactive)"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM customers")
                return cursor.fetchone()[0] or 0
        except Error as err:
            logger.error(f"Error getting total customers count: {err}")
            return 0

    def get_recent_customers(self, limit: int = 5) -> List[Dict]:
        """Get recent customers with detailed information"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        customer_id,
                        full_name AS name,
                        email,
                        phone,
                        status,
                        DATE_FORMAT(created_at, '%Y-%m-%d') AS signup_date
                    FROM customers
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                )
                return cursor.fetchall()
        except Error as err:
            logger.error(f"Error fetching recent customers: {err}")
            return []

    def get_customer_growth(self, months: int = 6) -> Dict[str, int]:
        """Get customer growth data for the last N months"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30*months)
            
            query = """
                SELECT 
                    DATE_FORMAT(created_at, '%Y-%m') AS month_group,
                    DATE_FORMAT(created_at, '%b') AS month,
                    COUNT(*) AS new_customers
                FROM customers
                WHERE created_at BETWEEN %s AND %s
                GROUP BY month_group, month
                ORDER BY month_group ASC
            """
            
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (start_date, end_date))
                results = cursor.fetchall()
                
            # Fill in missing months with 0 values
            all_months = {}
            current_date = start_date
            while current_date <= end_date:
                month_key = current_date.strftime('%b')
                all_months[month_key] = 0
                current_date += timedelta(days=30)
                
            # Update with actual data
            for row in results:
                all_months[row['month']] = int(row['new_customers'])
                
            return all_months
        except Error as err:
            logger.error(f"Error fetching customer growth data: {err}")
            return {}

    def get_revenue_trends(self, months: int = 6) -> Dict[str, float]:
        """Get revenue trends for the last N months"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30*months)
            
            query = """
                SELECT 
                    DATE_FORMAT(transaction_date, '%Y-%m') AS month_group,
                    DATE_FORMAT(transaction_date, '%b') AS month,
                    SUM(amount) AS revenue
                FROM transactions
                WHERE transaction_date BETWEEN %s AND %s
                GROUP BY month_group, month
                ORDER BY month_group ASC
            """
            
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (start_date, end_date))
                results = cursor.fetchall()
                
            # Fill in missing months
            all_months = {}
            current_date = start_date
            while current_date <= end_date:
                month_key = current_date.strftime('%b')
                all_months[month_key] = 0.0
                current_date += timedelta(days=30)
                
            for row in results:
                all_months[row['month']] = float(row['revenue'])
                
            return all_months
        except Error as err:
            logger.error(f"Error getting revenue trends: {err}")
            return {}

    def get_booking_trends(self, months: int = 6) -> Dict[str, int]:
        """Get booking trends for the last N months"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30*months)
            
            query = """
                SELECT 
                    DATE_FORMAT(created_at, '%Y-%m') AS month_group,
                    DATE_FORMAT(created_at, '%b') AS month,
                    COUNT(*) AS bookings
                FROM reservations
                WHERE created_at BETWEEN %s AND %s
                GROUP BY month_group, month
                ORDER BY month_group ASC
            """
            
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (start_date, end_date))
                results = cursor.fetchall()
                
            # Fill in missing months
            all_months = {}
            current_date = start_date
            while current_date <= end_date:
                month_key = current_date.strftime('%b')
                all_months[month_key] = 0
                current_date += timedelta(days=30)
                
            for row in results:
                all_months[row['month']] = int(row['bookings'])
                
            return all_months
        except Error as err:
            logger.error(f"Error getting booking trends: {err}")
            return {}

    # ========== CUSTOMER MANAGEMENT METHODS ==========
    def get_customers(self, status_filter: str = "all") -> List[Dict]:
        """Get customers with optional status filter"""
        try:
            query = "SELECT customer_id, full_name, email, address, phone, status FROM customers"
            params = ()

            if status_filter.lower() != "all":
                query += " WHERE status = %s"
                params = (status_filter.capitalize(),)

            query += " ORDER BY full_name ASC"

            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

        except Error as err:
            logger.error(f"Error fetching customers: {err}")
            return []

    def add_customer(self, customer_data: Dict) -> bool:
        """Add a new customer to the database"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO customers 
                    (customer_id, full_name, email, address, phone, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        customer_data["customer_id"],
                        customer_data["full_name"],
                        customer_data["email"],
                        customer_data["address"],
                        customer_data["phone"],
                        customer_data["status"],
                    ),
                )
                return True
        except Error as err:
            logger.error(f"Error adding customer: {err}")
            return False

    def update_customer(self, customer_id: str, updated_data: Dict) -> bool:
        """Update an existing customer"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE customers SET
                    full_name = %s,
                    email = %s,
                    address = %s,
                    phone = %s,
                    status = %s
                    WHERE customer_id = %s
                    """,
                    (
                        updated_data["full_name"],
                        updated_data["email"],
                        updated_data["address"],
                        updated_data["phone"],
                        updated_data["status"],
                        customer_id,
                    ),
                )
                return cursor.rowcount > 0
        except Error as err:
            logger.error(f"Error updating customer: {err}")
            return False

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer from the database"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM customers 
                    WHERE customer_id = %s
                    """,
                    (customer_id,),
                )
                return cursor.rowcount > 0
        except Error as err:
            logger.error(f"Error deleting customer: {err}")
            return False

    def search_customers(self, search_query: str) -> List[Dict]:
        """Search customers by name, email, address or phone"""
        try:
            query = """
                SELECT customer_id, full_name, email, address, phone, status 
                FROM customers 
                WHERE full_name LIKE %s 
                   OR email LIKE %s 
                   OR address LIKE %s 
                   OR phone LIKE %s
                ORDER BY full_name ASC
            """
            search_param = f"%{search_query}%"

            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    query, 
                    (search_param, search_param, search_param, search_param)
                )
                return cursor.fetchall()
        except Error as err:
            logger.error(f"Error searching customers: {err}")
            return []

    # ========== USER AUTHENTICATION METHODS ==========
    def register_user(
        self, full_name: str, email: str, password: str, gender: str
    ) -> Tuple[bool, str]:
        """Register a new user with comprehensive validation"""
        try:
            email = email.strip().lower()

            # Validate input
            if not all([full_name, email, password, gender]):
                return False, "All fields are required"

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return False, "Invalid email format"

            # Hash password consistently
            password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            logger.debug(f"Registering user {email} with hash: {password_hash[:8]}...")

            with self.connection.cursor() as cursor:
                # Check if email exists
                cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    return False, "Email already registered"

                # Insert new user
                cursor.execute(
                    """INSERT INTO users (full_name, email, password_hash, gender)
                    VALUES (%s, %s, %s, %s)""",
                    (full_name, email, password_hash, gender),
                )

                # Log the registration
                user_id = cursor.lastrowid
                self._log_auth_action(user_id, email, "register")

            return True, "Registration successful"

        except Error as err:
            logger.error(f"Registration failed for {email}: {err}")
            return False, "Registration failed"

    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user with enhanced security checks"""
        try:
            email = email.strip().lower()
            password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            logger.debug(f"Auth attempt for {email} with hash: {password_hash[:8]}...")

            with self.connection.cursor(dictionary=True) as cursor:
                # Get user with case-sensitive email comparison
                cursor.execute(
                    """
                    SELECT user_id, full_name, email, gender 
                    FROM users 
                    WHERE email = %s COLLATE utf8mb4_bin 
                    AND password_hash = %s
                    AND is_active = TRUE
                    """,
                    (email, password_hash),
                )

                user = cursor.fetchone()

                if user:
                    self._log_auth_action(user["user_id"], email, "login")
                    logger.info(f"Successful login for {email}")
                    return user
                else:
                    self._log_auth_action(None, email, "fail")
                    logger.warning(f"Failed login attempt for {email}")
                    return None

        except Error as err:
            logger.error(f"Authentication error for {email}: {err}")
            return None

    def _log_auth_action(self, user_id: Optional[int], email: str, action: str) -> None:
        """Log authentication attempts for security monitoring"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO auth_logs 
                    (user_id, email, action, ip_address, user_agent)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, email, action, "127.0.0.1", "Python App"),
                )
        except Error as err:
            logger.error(f"Failed to log auth action: {err}")

    def create_session(
        self, user_id: int, session_id: str, ip: str, user_agent: str, expires_at: str
    ) -> bool:
        """Create a new user session with validation"""
        try:
            expires_dt = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
            if expires_dt <= datetime.now():
                logger.error("Cannot create expired session")
                return False

            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO user_sessions 
                    (session_id, user_id, ip_address, user_agent, expires_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (session_id, user_id, ip, user_agent, expires_at),
                )

            return True
        except Error as err:
            logger.error(f"Session creation error: {err}")
            return False

    def verify_session(self, session_id: str) -> Optional[Dict]:
        """Verify if session is valid and return user data"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT u.user_id, u.full_name, u.email, u.gender
                    FROM user_sessions s
                    JOIN users u ON s.user_id = u.user_id
                    WHERE s.session_id = %s 
                    AND s.expires_at > NOW()
                    AND u.is_active = TRUE
                    """,
                    (session_id,),
                )

                return cursor.fetchone()
        except Error as err:
            logger.error(f"Session verification error: {err}")
            return None

    def close(self) -> None:
        """Close connection with proper resource cleanup"""
        if self.connection and self.connection.is_connected():
            try:
                self.connection.close()
                logger.info("Database connection closed")
            except Error as err:
                logger.error(f"Error closing connection: {err}")
        self.connection = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def hash_password(password: str) -> str:
    """Standardized password hashing using SHA-256 with UTF-8 encoding"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def populate_test_data(db):
    """Helper function to populate database with test data"""
    from datetime import datetime, timedelta
    import random

    # Add sample users
    db.register_user("Admin User", "admin@example.com", "admin123", "Male")

    # Add sample customers
    for i in range(1, 101):
        customer_id = f"CUST{1000 + i}"
        db.add_customer(
            {
                "customer_id": customer_id,
                "full_name": f"Customer {i}",
                "email": f"customer{i}@example.com",
                "address": f"{random.randint(1, 1000)} Main St",
                "phone": f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "status": "Active" if random.random() > 0.2 else "Inactive",
            }
        )

    # Add sample reservations
    for i in range(200):
        reservation_id = f"RES{10000 + i}"
        user_id = 1  # Admin user
        guest_name = f"Guest {i}"
        checkin_date = datetime.now() + timedelta(days=random.randint(1, 30))
        checkout_date = checkin_date + timedelta(days=random.randint(1, 14))
        booking_amount = random.randint(50, 500)
        payment_status = random.choice(["Paid", "Pending", "Cancelled"])
        fulfillment_status = random.choice(["Confirmed", "Pending", "Cancelled"])

        db.connection.cursor().execute(
            """
            INSERT INTO reservations (
                reservation_id, user_id, guest_name, 
                checkin_date, checkout_date, booking_amount,
                payment_status, fulfillment_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                reservation_id,
                user_id,
                guest_name,
                checkin_date,
                checkout_date,
                booking_amount,
                payment_status,
                fulfillment_status,
            ),
        )

    # Add sample transactions
    for i in range(200):
        amount = random.randint(50, 500)
        days_ago = random.randint(0, 180)
        transaction_date = datetime.now() - timedelta(days=days_ago)
        customer_id = f"CUST{random.randint(1001, 1100)}"
        reservation_id = f"RES{random.randint(10000, 10199)}"

        db.connection.cursor().execute(
            """
            INSERT INTO transactions (customer_id, reservation_id, amount, transaction_date)
            VALUES (%s, %s, %s, %s)
            """,
            (customer_id, reservation_id, amount, transaction_date),
        )

    # Add sample occupancy data
    start_date = datetime.now() - timedelta(days=180)
    for i in range(180):
        date = start_date + timedelta(days=i)
        occupied = random.randint(70, 95)
        total = 100

        db.connection.cursor().execute(
            """
            INSERT INTO room_occupancy (date, occupied_rooms, total_rooms)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                occupied_rooms = VALUES(occupied_rooms),
                total_rooms = VALUES(total_rooms)
            """,
            (date.date(), occupied, total),
        )

    db.connection.commit()
    print("Test data populated successfully")


if __name__ == "__main__":
    # Initialize database and populate test data
    with DatabaseManager() as db:
        # Uncomment to populate test data
        # populate_test_data(db)

        # Test dashboard methods
        print("\n=== Dashboard Statistics ===")
        print("Total Bookings Cost:", db.get_total_bookings_cost())
        print("Total Reservations:", db.get_total_reservations())
        print("Active Customers:", db.get_active_customers_count())
        print("Total Customers:", db.get_total_customers())
        
        print("\n=== Recent Customers ===")
        for customer in db.get_recent_customers():
            print(f"{customer['name']} ({customer['email']})")
            
        print("\n=== Customer Growth ===")
        print(db.get_customer_growth())
        
        print("\n=== Revenue Trends ===")
        print(db.get_revenue_trends())
        
        print("\n=== Booking Trends ===")
        print(db.get_booking_trends())