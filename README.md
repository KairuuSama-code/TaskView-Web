# TaskView Web Application

A web-based activity management system for teachers and students, converted from Tkinter desktop application to Flask web application while maintaining the **exact original flow**.

## 📋 System Overview

TaskView allows teachers to post activities and students to view them, organized by sections.

### For Teachers:
- ✅ Register with teacher PIN verification
- ✅ Login to access system
- ✅ Select section to manage
- ✅ Post activities with attachments
- ✅ Delete only their own activities
- ✅ View all activities in a section

### For Students:
- ✅ Select their section
- ✅ Enter section PIN to access
- ✅ View all activities in their section
- ✅ Download activity attachments
- ✅ Read-only access (cannot post or delete)

## 🎯 Key Difference from Standard Web Apps

**Students DO NOT have accounts!**
- No student registration
- No student login
- Students only need to know their section PIN
- Teachers have accounts with passwords

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install flask werkzeug

# Run the application
python app.py
```

Access at: `http://localhost:5000`

## 🔐 Default Credentials

### Teacher PIN (for registration):
```
PIN: 1234
```

### Section PINs (for students):
```
Grade 11 - ICT - CHRONICLES: 1111
Grade 11 - ICT - HAGGAI:     2222
Grade 12 - ICT - JUDE:       3333
Grade 12 - ICT - TITUS:      4444
Grade 11 - STEM:             5555
Grade 12 - STEM:             6666
Grade 11 - HUMSS:            7777
Grade 12 - HUMSS:            8888
Grade 11 - HE:               9999
Grade 12 - HE - EZRA:        0000
```

## 📱 User Flow

### Teacher Flow:
1. Click "Teacher" on role selection
2. **Register** (first time):
   - Enter name
   - Create password
   - Enter teacher PIN (1234)
3. **Login**:
   - Enter name and password
4. **Select Section** to manage
5. **View Activities** for that section
6. **Add Activity**:
   - Enter subject, type, deadline
   - Write description
   - Upload file (optional)
   - Post to section
7. **View/Delete** your own activities

### Student Flow:
1. Click "Student" on role selection
2. **Select Section** from dropdown
3. **Enter Section PIN**
4. **View Activities** (read-only)
5. **Click activity** to see details
6. **Download attachments** if available

## 📁 Project Structure

```
taskview-web/
├── app.py                          # Main Flask application
├── taskview.db                     # SQLite database
├── requirements.txt                # Dependencies
│
├── templates/                      # HTML pages
│   ├── role_selection.html         # Start screen
│   ├── teacher_register.html       # Teacher signup
│   ├── teacher_login.html          # Teacher login
│   ├── teacher_section_selection.html
│   ├── teacher_activities.html     # Activity list (teacher)
│   ├── add_activity.html           # Create activity
│   ├── student_section_selection.html
│   ├── student_activities.html     # Activity list (student)
│   └── activity_detail.html        # Full activity view
│
└── static/
    ├── css/
    │   └── styles.css              # Styling
    ├── images/
    │   └── tfucslogo.png           # Logo
    └── uploads/                    # Uploaded files
```

## 🗄️ Database Schema

### Teachers Table
```sql
- id (PRIMARY KEY)
- name (UNIQUE)
- password (HASHED)
- created_at
```

### Activities Table
```sql
- id (PRIMARY KEY)
- section
- subject
- type (Quiz, Assignment, etc.)
- deadline
- description
- attachment (filename)
- teacher_id (FOREIGN KEY)
- teacher_name
- created_at
```

**Note:** No students table - students don't have accounts!

## ⚙️ Configuration

Edit in `app.py`:

```python
# Secret key (CHANGE THIS!)
app.secret_key = 'your-secret-key-here'

# Teacher PIN for registration
TEACHER_PIN = "1234"

# Section PINs
SECTION_PINS = {
    "Grade 11 - ICT - CHRONICLES": "1111",
    "Grade 11 - ICT - HAGGAI": "2222",
    # ... add more sections
}

# File upload settings
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## 🌐 Deployment to Replit

1. Go to https://replit.com
2. Create new Python Repl
3. Upload all project files
4. Click "Run"
5. Share your Repl URL!

**See REPLIT_DEPLOYMENT.md for detailed instructions.**

## 🔒 Security Features

- ✅ Password hashing (Werkzeug)
- ✅ Session management
- ✅ Teacher PIN verification
- ✅ Section PIN verification
- ✅ Activity ownership validation
- ✅ Secure file upload handling
- ✅ SQL injection protection

## 🎨 Customization

### Add/Change Sections:
Edit `SECTION_PINS` dictionary in `app.py`

### Change Teacher PIN:
Edit `TEACHER_PIN` in `app.py`

### Change File Upload Limits:
Edit `ALLOWED_EXTENSIONS` and `MAX_CONTENT_LENGTH` in `app.py`

### Update Styling:
Edit `static/css/styles.css`

## 🐛 Troubleshooting

**Can't register as teacher:**
- Make sure you're using correct teacher PIN (1234)

**Student can't access section:**
- Check section PIN is correct
- Verify section exists in SECTION_PINS

**Can't delete activity:**
- Only the teacher who posted can delete
- Other teachers can view but not delete

**File upload fails:**
- Check file size < 16MB
- Verify file type is allowed
- Ensure `static/uploads/` folder exists

## 📚 Documentation

- **SYSTEM_FLOW.md** - Complete user flow diagrams
- **CONVERSION_GUIDE.md** - Tkinter → Flask conversion details
- **REPLIT_DEPLOYMENT.md** - Deploy to Replit guide

## 🎓 For Capstone Presentation

### Demo Preparation:
1. Deploy to Replit before presentation
2. Create test teacher account
3. Post sample activities
4. Test student PIN access
5. Prepare screenshots as backup

### Talking Points:
- "Converted from desktop to web application"
- "Maintains original workflow exactly"
- "Accessible from any device"
- "Multiple users simultaneously"
- "Secure PIN-based access"
- "No student accounts needed"

## 👥 Team Workflow

1. **Backend dev:** Test all routes work
2. **Frontend dev:** Update CSS styling
3. **Both:** Test complete flow together
4. **Deploy:** Upload to Replit
5. **Present:** Demo live application

## 📄 License

Educational project for TFUCS

---

**Successfully converted from Tkinter to Flask while maintaining the exact original user flow!** 🎉
