# Step 1: Setting Up the Database (SQLite)
# Here’s a sample SQLite schema based on your requirements. You can use SQLAlchemy (an ORM for Python) to handle database interactions.
#
# python
# Copy code
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_amount_to_pay = db.Column(db.Float, nullable=False)
    actual_amount_paid = db.Column(db.Float, default=0.0)
    balance_due = db.Column(db.Float, default=0.0)
    study_type = db.Column(db.String(100))  # e.g., Standard, Intensive, OBU Mentoring
    papers_enrolled = db.Column(db.String(200))
    deferred = db.Column(db.Boolean, default=False)
    video_request_status = db.Column(db.String(50), default='Pending')  # Pending, Approved, Denied
    video_request_date = db.Column(db.DateTime, default=datetime.utcnow)
    refund_amount = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Student {self.name}>"

# Initialize database
with app.app_context():
    db.create_all()
# Step 2: API Endpoints
# These endpoints will allow you to handle core actions, like updating payments, managing video requests, and updating student enrollment.
#
# python
# Copy code
from flask import jsonify, request

# Fetch all students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{
        'id': student.id,
        'name': student.name,
        'total_amount_to_pay': student.total_amount_to_pay,
        'actual_amount_paid': student.actual_amount_paid,
        'balance_due': student.balance_due,
        'study_type': student.study_type,
        'papers_enrolled': student.papers_enrolled,
        'deferred': student.deferred,
        'video_request_status': student.video_request_status,
        'video_request_date': student.video_request_date,
        'refund_amount': student.refund_amount
    } for student in students])

# Update payment
@app.route('/students/<int:id>/payment', methods=['PUT'])
def update_payment(id):
    data = request.json
    student = Student.query.get_or_404(id)
    amount_paid = data.get('amount_paid')
    student.actual_amount_paid += amount_paid
    student.balance_due = student.total_amount_to_pay - student.actual_amount_paid
    db.session.commit()
    return jsonify({'message': 'Payment updated', 'balance_due': student.balance_due})

# Update video request status
@app.route('/students/<int:id>/video-request', methods=['PUT'])
def update_video_request(id):
    data = request.json
    student = Student.query.get_or_404(id)
    student.video_request_status = data.get('status')
    db.session.commit()
    return jsonify({'message': 'Video request status updated', 'status': student.video_request_status})

@app.route("/")
def homepage():
    return render_template("too_temp.html")

if __name__ == "__main__":
    app.run(debug=True)