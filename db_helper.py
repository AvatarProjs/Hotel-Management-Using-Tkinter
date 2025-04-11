import mysql.connector
from mysql.connector import Error, errorcode
from dotenv import load_dotenv
import os
import hashlib
import re
from typing import Optional, Dict, Tuple
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
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
                    ssl_disabled=False,  # SSL enabled without cert verification
                    connect_timeout=5,
                    connection_timeout=30,
                    autocommit=True,
                    pool_name="hotel_pool",
                    pool_size=5
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
            'users': """
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
            'user_sessions': """
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id VARCHAR(255) PRIMARY KEY,
                    user_id INT NOT NULL,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                ) ENGINE=InnoDB
            """,
            'auth_logs': """
                CREATE TABLE IF NOT EXISTS auth_logs (
                    log_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NULL,
                    email VARCHAR(100) NOT NULL,
                    action ENUM('register','login','logout','fail') NOT NULL,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
                ) ENGINE=InnoDB
            """
        }

        try:
            with self.connection.cursor() as cursor:
                for table_name, ddl in tables.items():
                    try:
                        cursor.execute(ddl)
                        logger.info(f"Table '{table_name}' verified")
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

    def register_user(self, full_name: str, email: str, password: str, gender: str) -> Tuple[bool, str]:
        """Register a new user with comprehensive validation"""
        try:
            email = email.strip().lower()
            
            # Validate input
            if not all([full_name, email, password, gender]):
                return False, "All fields are required"
                
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return False, "Invalid email format"

            # Hash password consistently
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
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
                    (full_name, email, password_hash, gender)
                )
                
                # Log the registration
                user_id = cursor.lastrowid
                self._log_auth_action(user_id, email, 'register')
                
            return True, "Registration successful"
            
        except Error as err:
            logger.error(f"Registration failed for {email}: {err}")
            return False, "Registration failed"
            
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user with enhanced security checks"""
        try:
            email = email.strip().lower()
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            logger.debug(f"Auth attempt for {email} with hash: {password_hash[:8]}...")

            with self.connection.cursor(dictionary=True) as cursor:
                # Get user with case-sensitive email comparison
                cursor.execute("""
                    SELECT user_id, full_name, email, gender 
                    FROM users 
                    WHERE email = %s COLLATE utf8mb4_bin 
                    AND password_hash = %s
                    AND is_active = TRUE
                """, (email, password_hash))
                
                user = cursor.fetchone()
                
                if user:
                    self._log_auth_action(user['user_id'], email, 'login')
                    logger.info(f"Successful login for {email}")
                    return user
                else:
                    self._log_auth_action(None, email, 'fail')
                    logger.warning(f"Failed login attempt for {email}")
                    return None
                    
        except Error as err:
            logger.error(f"Authentication error for {email}: {err}")
            return None

    def _log_auth_action(self, user_id: Optional[int], email: str, action: str) -> None:
        """Log authentication attempts for security monitoring"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO auth_logs 
                    (user_id, email, action, ip_address, user_agent)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, email, action, '127.0.0.1', 'Python App'))
        except Error as err:
            logger.error(f"Failed to log auth action: {err}")

    def create_session(self, user_id: int, session_id: str, ip: str, user_agent: str, expires_at: str) -> bool:
        """Create a new user session with validation"""
        try:
            expires_dt = datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S')
            if expires_dt <= datetime.now():
                logger.error("Cannot create expired session")
                return False

            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user_sessions 
                    (session_id, user_id, ip_address, user_agent, expires_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (session_id, user_id, ip, user_agent, expires_at))
                
            return True
        except Error as err:
            logger.error(f"Session creation error: {err}")
            return False

    def verify_session(self, session_id: str) -> Optional[Dict]:
        """Verify if session is valid and return user data"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT u.user_id, u.full_name, u.email, u.gender
                    FROM user_sessions s
                    JOIN users u ON s.user_id = u.user_id
                    WHERE s.session_id = %s 
                    AND s.expires_at > NOW()
                    AND u.is_active = TRUE
                """, (session_id,))
                
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

# Consistent password hashing for the entire application
def hash_password(password: str) -> str:
    """Standardized password hashing using SHA-256 with UTF-8 encoding"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    # Test database connection and basic operations
    with DatabaseManager() as db:
        # Test registration
        test_email = "test_user@example.com"
        test_pass = "SecurePassword123!"
        
        # Cleanup previous test data
        with db.connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (test_email,))
            db.connection.commit()
        
        # Test registration
        success, message = db.register_user(
            "Test User", 
            test_email, 
            test_pass, 
            "Male"
        )
        print(f"Registration: {success} - {message}")
        
        # Test authentication
        user = db.authenticate_user(test_email, test_pass)
        print(f"Authentication: {bool(user)}")
        
        # Test failed authentication
        user = db.authenticate_user(test_email, "wrongpassword")
        print(f"Failed auth: {not user}")
        
        # Test session management
        if user:
            session_id = "test_session_123"
            expires_at = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            if db.create_session(user['user_id'], session_id, "127.0.0.1", "Python Test", expires_at):
                print("Session created successfully")
                print("Session valid:", bool(db.verify_session(session_id)))