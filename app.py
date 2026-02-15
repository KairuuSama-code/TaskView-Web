from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# ================= CONFIGURATION =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "taskview.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= PINS =================
TEACHER_PIN = "1234"
SECTION_PINS = {
    "Grade 11 - ICT - CHRONICLES": "1111",
    "Grade 11 - ICT - HAGGAI": "2222",
    "Grade 12 - ICT - JUDE": "3333",
    "Grade 12 - ICT - TITUS": "4444",
    "Grade 11 - STEM - JOEL": "5555",
    "Grade 12 - STEM - THESSALONIANS": "6666",
    "Grade 11 - HUMSS - JUDGES": "7777",
    "Grade 12 - HUMSS -LEVITICUS": "8888",
    "Grade 11 - HE - MICAH": "9999",
    "Grade 12 - HE - EZRA": "0000"
}

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL,
            subject TEXT NOT NULL,
            type TEXT NOT NULL,
            deadline TEXT,
            description TEXT,
            attachment TEXT,
            teacher_id INTEGER,
            teacher_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

# ================= HELPERS =================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def teacher_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'teacher_id' not in session:
            return redirect(url_for('teacher_login'))
        return f(*args, **kwargs)
    return decorated

# ================= ROUTES =================

@app.route('/')
def index():
    session.clear()
    return render_template('role_selection.html')

# ========== TEACHER FLOW ==========

@app.route('/teacher/register', methods=['GET', 'POST'])
def teacher_register():
    if request.method == 'GET':
        return render_template('teacher_register.html')
    
    data = request.get_json()
    name = data.get('name')
    teacher_pin = data.get('teacher_pin')
    password = data.get('password')
    
    if teacher_pin != TEACHER_PIN:
        return jsonify({'error': 'Invalid teacher PIN'}), 401
    
    try:
        conn = get_db()
        hashed = generate_password_hash(password)
        conn.execute('INSERT INTO teachers (name, password) VALUES (?, ?)', (name, hashed))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Teacher name already exists'}), 400

@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'GET':
        return render_template('teacher_login.html')
    
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    
    conn = get_db()
    teacher = conn.execute('SELECT * FROM teachers WHERE name = ?', (name,)).fetchone()
    conn.close()
    
    if teacher and check_password_hash(teacher['password'], password):
        session['teacher_id'] = teacher['id']
        session['teacher_name'] = teacher['name']
        session['role'] = 'teacher'
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/teacher/section-select')
@teacher_login_required
def teacher_section_select():
    return render_template('teacher_section_select.html', sections=list(SECTION_PINS.keys()))

@app.route('/teacher/activities/<section>')
@teacher_login_required
def teacher_activities(section):
    if section not in SECTION_PINS:
        return redirect(url_for('teacher_section_select'))
    
    session['current_section'] = section
    
    conn = get_db()
    activities = conn.execute(
        'SELECT * FROM activities WHERE section = ? ORDER BY created_at DESC',
        (section,)
    ).fetchall()
    conn.close()
    
    return render_template('teacher_activities.html', 
                         activities=activities, 
                         section=section,
                         teacher_name=session['teacher_name'])

@app.route('/teacher/add-activity', methods=['GET', 'POST'])
@teacher_login_required
def teacher_add_activity():
    if request.method == 'GET':
        section = session.get('current_section', '')
        return render_template('add_activity.html', section=section)
    
    section = request.form.get('section')
    subject = request.form.get('subject')
    type_ = request.form.get('type')
    deadline = request.form.get('deadline')
    description = request.form.get('description')
    
    attachment = None
    if 'attachment' in request.files:
        file = request.files['attachment']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            attachment = filename
    
    conn = get_db()
    conn.execute(
        '''INSERT INTO activities 
           (section, subject, type, deadline, description, attachment, teacher_id, teacher_name)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (section, subject, type_, deadline, description, attachment,
         session['teacher_id'], session['teacher_name'])
    )
    conn.commit()
    conn.close()
    
    return redirect(url_for('teacher_activities', section=section))

@app.route('/teacher/activity/<int:activity_id>')
@teacher_login_required
def teacher_view_activity(activity_id):
    conn = get_db()
    activity = conn.execute('SELECT * FROM activities WHERE id = ?', (activity_id,)).fetchone()
    conn.close()
    
    if not activity:
        return "Activity not found", 404
    
    can_delete = (activity['teacher_id'] == session['teacher_id'])
    
    return render_template('activity_detail.html', 
                         activity=activity, 
                         can_delete=can_delete,
                         is_teacher=True)

@app.route('/teacher/delete-activity/<int:activity_id>', methods=['POST'])
@teacher_login_required
def teacher_delete_activity(activity_id):
    conn = get_db()
    activity = conn.execute(
        'SELECT * FROM activities WHERE id = ? AND teacher_id = ?',
        (activity_id, session['teacher_id'])
    ).fetchone()
    
    if activity:
        if activity['attachment']:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], activity['attachment'])
            if os.path.exists(filepath):
                os.remove(filepath)
        
        conn.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
        conn.commit()
    
    conn.close()
    section = session.get('current_section', '')
    return redirect(url_for('teacher_activities', section=section))

# ========== STUDENT FLOW ==========

@app.route('/student/section-select')
def student_section_select():
    session['role'] = 'student'
    return render_template('student_section_select.html', sections=list(SECTION_PINS.keys()))

@app.route('/student/verify-pin', methods=['POST'])
def student_verify_pin():
    data = request.get_json()
    section = data.get('section')
    pin = data.get('pin')
    
    if section not in SECTION_PINS:
        return jsonify({'error': 'Invalid section'}), 400
    
    if pin != SECTION_PINS[section]:
        return jsonify({'error': 'Incorrect PIN'}), 401
    
    session['student_section'] = section
    session['role'] = 'student'
    return jsonify({'success': True, 'section': section})

@app.route('/student/activities')
def student_activities():
    if session.get('role') != 'student' or 'student_section' not in session:
        return redirect(url_for('student_section_select'))
    
    section = session['student_section']
    
    conn = get_db()
    activities = conn.execute(
        'SELECT * FROM activities WHERE section = ? ORDER BY created_at DESC',
        (section,)
    ).fetchall()
    conn.close()
    
    return render_template('student_activities.html', 
                         activities=activities,
                         section=section)

@app.route('/student/activity/<int:activity_id>')
def student_view_activity(activity_id):
    if session.get('role') != 'student':
        return redirect(url_for('index'))
    
    conn = get_db()
    activity = conn.execute('SELECT * FROM activities WHERE id = ?', (activity_id,)).fetchone()
    conn.close()
    
    if not activity:
        return "Activity not found", 404
    
    if activity['section'] != session.get('student_section'):
        return "Access denied", 403
    
    return render_template('activity_detail.html', 
                         activity=activity,
                         can_delete=False,
                         is_teacher=False)

# ========== COMMON ==========

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/sections')
def get_sections():
    return jsonify(list(SECTION_PINS.keys()))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
