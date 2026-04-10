"""
==========================================================
  Student Management System
  Flask + Apache Cassandra (Column-Family NoSQL)
==========================================================
"""

from cassandra.cluster import Cluster
from flask import Flask, render_template, request, redirect, url_for, flash
import time
import os

app = Flask(__name__)
app.secret_key = 'student-cassandra-secret-key'

# Global database variables
cluster = None
session = None

def get_db():
    global cluster, session
    if session is None:
        cluster = Cluster(['127.0.0.1'], port=9042)
        session = cluster.connect()
        session.set_keyspace('university')
    return cluster, session

def init_database():
    max_retries = 15
    for attempt in range(max_retries):
        try:
            # ใช้ local cluster/session สำหรับการ init
            temp_cluster = Cluster(['127.0.0.1'], port=9042)
            temp_session = temp_cluster.connect()

            temp_session.execute("""
                CREATE KEYSPACE IF NOT EXISTS university
                WITH replication = {
                    'class': 'SimpleStrategy',
                    'replication_factor': 1
                }
            """)

            temp_session.set_keyspace('university')

            temp_session.execute("""
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

            print("Database พร้อมใช้งาน!")
            temp_cluster.shutdown()
            return True

        except Exception as e:
            print(f"รอ Cassandra... ({attempt + 1}/{max_retries}) - {e}")
            time.sleep(5)

    print("ไม่สามารถเชื่อมต่อ Cassandra ได้")
    return False


@app.route('/')
def index():
    try:
        _, db_session = get_db()
        rows = db_session.execute("SELECT * FROM students")
        students = []
        for row in rows:
            students.append({
                'student_id': row.student_id,
                'first_name': row.first_name,
                'last_name': row.last_name,
                'email': row.email,
                'department': row.department,
                'gpa': row.gpa,
                'year': row.year
            })

        students.sort(key=lambda x: x['student_id'])
        return render_template('index.html', students=students)

    except Exception as e:
        return f"Error: {e}"


@app.route('/create', methods=['POST'])
def create():
    try:
        student_id = request.form['student_id'].strip()
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        email = request.form['email'].strip()
        department = request.form['department'].strip()
        gpa = float(request.form['gpa'])
        year = int(request.form['year'])

        _, db_session = get_db()
        query = db_session.prepare("""
            INSERT INTO students (student_id, first_name, last_name, email, department, gpa, year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """)
        db_session.execute(query, (student_id, first_name, last_name, email, department, gpa, year))

        flash(f'เพิ่มนักศึกษา {first_name} {last_name} สำเร็จ!', 'success')

    except Exception as e:
        flash(f'เกิดข้อผิดพลาด: {e}', 'danger')

    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    try:
        student_id = request.form['student_id']
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        email = request.form['email'].strip()
        department = request.form['department'].strip()
        gpa = float(request.form['gpa'])
        year = int(request.form['year'])

        _, db_session = get_db()
        query = db_session.prepare("""
            UPDATE students
            SET first_name = ?, last_name = ?, email = ?, department = ?, gpa = ?, year = ?
            WHERE student_id = ?
        """)
        db_session.execute(query, (first_name, last_name, email, department, gpa, year, student_id))

        flash(f'แก้ไขข้อมูลรหัส {student_id} สำเร็จ!', 'success')

    except Exception as e:
        flash(f'เกิดข้อผิดพลาด: {e}', 'danger')

    return redirect(url_for('index'))


@app.route('/delete/<student_id>')
def delete(student_id):
    try:
        _, db_session = get_db()
        db_session.execute(
            db_session.prepare("DELETE FROM students WHERE student_id = ?"),
            (student_id,)
        )

        flash(f'ลบนักศึกษารหัส {student_id} สำเร็จ!', 'success')

    except Exception as e:
        flash(f'เกิดข้อผิดพลาด: {e}', 'danger')

    return redirect(url_for('index'))


if __name__ == '__main__':
    # ป้องกันการรันซ้ำเมื่อใช้ Flask Debug Mode reloader
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        print("กำลังเริ่มต้น Student Management System...")
        init_database()
        
    print("เปิดเว็บที่: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)