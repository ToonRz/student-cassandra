"""
==========================================================
  CRUD Demo - Apache Cassandra (Column-Family NoSQL)
  ระบบจัดการนักศึกษา (Student Management System)
==========================================================
"""

from cassandra.cluster import Cluster
import time


def wait_for_cassandra(max_retries=10, delay=5):
    for attempt in range(max_retries):
        try:
            cluster = Cluster(['127.0.0.1'], port=9042)
            session = cluster.connect()
            print("เชื่อมต่อ Cassandra สำเร็จ!")
            return cluster, session
        except Exception as e:
            print(f"รอ Cassandra... (ครั้งที่ {attempt + 1}/{max_retries}) - {e}")
            time.sleep(delay)
    print("ไม่สามารถเชื่อมต่อ Cassandra ได้")
    exit(1)


def setup_database(session):
    print("\n" + "=" * 60)
    print("SETUP: สร้าง Keyspace และ Table")
    print("=" * 60)

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS university
        WITH replication = {
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }
    """)
    print("สร้าง Keyspace 'university' สำเร็จ")

    session.set_keyspace('university')

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
    print("สร้าง Table 'students' สำเร็จ")

    session.execute("TRUNCATE students")
    print("ล้างข้อมูลเก่าเรียบร้อย")


def demo_create(session):
    print("\n" + "=" * 60)
    print("CREATE: เพิ่มข้อมูลนักศึกษา")
    print("=" * 60)

    students = [
        ('6501001', 'สมชาย', 'ใจดี', 'somchai@uni.ac.th', 'วิทยาการคอมพิวเตอร์', 3.25, 2),
        ('6501002', 'สมหญิง', 'รักเรียน', 'somying@uni.ac.th', 'วิศวกรรมซอฟต์แวร์', 3.75, 3),
        ('6501003', 'วิชัย', 'เก่งมาก', 'wichai@uni.ac.th', 'เทคโนโลยีสารสนเทศ', 2.90, 1),
        ('6501004', 'มานี', 'สวยงาม', 'manee@uni.ac.th', 'วิทยาการคอมพิวเตอร์', 3.50, 4),
        ('6501005', 'ปิติ', 'สุขใจ', 'piti@uni.ac.th', 'วิศวกรรมซอฟต์แวร์', 3.10, 2),
    ]

    insert_query = session.prepare("""
        INSERT INTO students (student_id, first_name, last_name, email, department, gpa, year)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """)

    for student in students:
        session.execute(insert_query, student)
        print(f"  เพิ่ม: {student[0]} - {student[1]} {student[2]}")

    print(f"\nเพิ่มข้อมูลทั้งหมด {len(students)} คน สำเร็จ!")


def demo_read(session):
    print("\n" + "=" * 60)
    print("READ: อ่านข้อมูลนักศึกษา")
    print("=" * 60)

    print("\n--- 1) อ่านข้อมูลทั้งหมด ---")
    rows = session.execute("SELECT * FROM students")

    for row in rows:
        print(f"  {row.student_id} | {row.first_name} {row.last_name} | "
              f"{row.department} | GPA: {row.gpa} | ปี {row.year}")

    print("\n--- 2) ค้นหานักศึกษารหัส 6501002 ---")
    row = session.execute(
        "SELECT * FROM students WHERE student_id = '6501002'"
    ).one()

    if row:
        print(f"  รหัส: {row.student_id}")
        print(f"  ชื่อ: {row.first_name} {row.last_name}")
        print(f"  อีเมล: {row.email}")
        print(f"  ภาควิชา: {row.department}")
        print(f"  GPA: {row.gpa}")
        print(f"  ชั้นปี: {row.year}")


def demo_update(session):
    print("\n" + "=" * 60)
    print("UPDATE: แก้ไขข้อมูลนักศึกษา")
    print("=" * 60)

    print("\n--- ข้อมูลก่อนแก้ไข (รหัส 6501003) ---")
    row = session.execute(
        "SELECT * FROM students WHERE student_id = '6501003'"
    ).one()
    print(f"  ชื่อ: {row.first_name} {row.last_name}")
    print(f"  GPA: {row.gpa}")
    print(f"  ชั้นปี: {row.year}")

    session.execute("""
        UPDATE students
        SET gpa = 3.45, year = 2
        WHERE student_id = '6501003'
    """)
    print("\n  อัปเดต GPA เป็น 3.45 และชั้นปีเป็น 2...")

    print("\n--- ข้อมูลหลังแก้ไข (รหัส 6501003) ---")
    row = session.execute(
        "SELECT * FROM students WHERE student_id = '6501003'"
    ).one()
    print(f"  ชื่อ: {row.first_name} {row.last_name}")
    print(f"  GPA: {row.gpa}")
    print(f"  ชั้นปี: {row.year}")
    print("\n  อัปเดตสำเร็จ!")


def demo_delete(session):
    print("\n" + "=" * 60)
    print("DELETE: ลบข้อมูลนักศึกษา")
    print("=" * 60)

    rows_before = list(session.execute("SELECT * FROM students"))
    print(f"\n  จำนวนนักศึกษาก่อนลบ: {len(rows_before)} คน")

    print("\n--- จะลบนักศึกษารหัส 6501005 ---")
    row = session.execute(
        "SELECT * FROM students WHERE student_id = '6501005'"
    ).one()
    print(f"  ลบ: {row.student_id} - {row.first_name} {row.last_name}")

    session.execute("DELETE FROM students WHERE student_id = '6501005'")
    print("\n  กำลังลบ...")

    rows_after = list(session.execute("SELECT * FROM students"))
    print(f"  จำนวนนักศึกษาหลังลบ: {len(rows_after)} คน")

    print("\n--- ข้อมูลที่เหลือ ---")
    for row in rows_after:
        print(f"  {row.student_id} - {row.first_name} {row.last_name}")

    print("\n  ลบสำเร็จ!")


if __name__ == "__main__":
    print("เริ่มต้น CRUD Demo - Apache Cassandra")
    print("=" * 60)

    cluster, session = wait_for_cassandra()

    try:
        setup_database(session)
        demo_create(session)
        demo_read(session)
        demo_update(session)
        demo_delete(session)

        print("\n" + "=" * 60)
        print("CRUD Demo เสร็จสมบูรณ์!")
        print("=" * 60)

    finally:
        cluster.shutdown()
        print("\nปิดการเชื่อมต่อเรียบร้อย")