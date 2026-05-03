import random
from cassandra.cluster import Cluster
from faker import Faker
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Initialize Faker
fake = Faker()

# Configuration
CASSANDRA_HOSTS = ['127.0.0.1']
CASSANDRA_PORT = 9042
KEYSPACE = 'university'
TOTAL_RECORDS = 100000
BATCH_SIZE = 1000  # Show progress every 1000 records

DEPARTMENTS = [
    'Computer Science', 'Information Technology', 'Software Engineering',
    'Data Science', 'Artificial Intelligence', 'Cyber Security',
    'Mechanical Engineering', 'Electrical Engineering', 'Civil Engineering',
    'Business Administration', 'Digital Marketing', 'Accounting'
]

def generate_student():
    return {
        'student_id': f"STD{fake.unique.random_number(digits=8, fix_len=True)}",
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'department': random.choice(DEPARTMENTS),
        'gpa': round(random.uniform(2.0, 4.0), 2),
        'year': random.randint(1, 4)
    }

def insert_data():
    try:
        cluster = Cluster(CASSANDRA_HOSTS, port=CASSANDRA_PORT)
        session = cluster.connect()
        
        # Ensure keyspace exists
        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
        """)
        session.set_keyspace(KEYSPACE)
        
        # Ensure table exists
        session.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                department TEXT,
                gpa FLOAT,
                year INT
            )
        """)

        print(f"Starting to insert {TOTAL_RECORDS} records...")
        
        query = session.prepare("""
            INSERT INTO students (student_id, first_name, last_name, email, department, gpa, year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """)

        start_time = time.time()
        
        # Using execute_async for performance
        futures = []
        for i in range(1, TOTAL_RECORDS + 1):
            student = generate_student()
            future = session.execute_async(query, (
                student['student_id'],
                student['first_name'],
                student['last_name'],
                student['email'],
                student['department'],
                student['gpa'],
                student['year']
            ))
            futures.append(future)
            
            # Periodically wait for results to avoid memory issues with too many futures
            if i % 2000 == 0:
                for f in futures:
                    f.result() # Wait for completion
                futures = []
                elapsed = time.time() - start_time
                print(f"Inserted {i}/{TOTAL_RECORDS} records... ({elapsed:.2f}s)")

        # Wait for any remaining futures
        for f in futures:
            f.result()

        end_time = time.time()
        print(f"\nSuccessfully inserted {TOTAL_RECORDS} records in {end_time - start_time:.2f} seconds.")
        
        # Verify count
        result = session.execute("SELECT COUNT(*) FROM students")
        print(f"Total records in 'students' table: {result[0].count}")
        
        cluster.shutdown()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    insert_data()
