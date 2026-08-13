from flask import Flask, request
from database import initialize_database, get_db

app = Flask(__name__)

initialize_database()


@app.route("/")
def home():
    return """
    <h1>Hospital Management System</h1>

    <h3>Available Modules</h3>
    <ul>
    	<li><a href="/register">Patient Registration</a></li>
    	<li><a href="/appointments">Appointments</a></li>
    	<li><a href="/prescriptions">Prescriptions</a></li>
    	<li><a href="/billing">Billing</a></li>
    	<li><a href="/medical-records">Medical Records</a></li>
    </ul>
    """


@app.route("/register", methods=["GET", "POST"])
def register_patient():

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        phone = request.form["phone"]
        address = request.form["address"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO patients (name, age, phone, address)
            VALUES (?, ?, ?, ?)
            """,
            (name, age, phone, address)
        )

        conn.commit()
        conn.close()

        return "<h2>Patient registered successfully!</h2><a href='/'>Back to Home</a>"

    return """
    <h1>Patient Registration</h1>

    <form method="POST">

        <label>Name:</label><br>
        <input type="text" name="name"><br><br>

        <label>Age:</label><br>
        <input type="number" name="age"><br><br>

        <label>Phone:</label><br>
        <input type="text" name="phone"><br><br>

        <label>Address:</label><br>
        <input type="text" name="address"><br><br>

        <button type="submit">Register Patient</button>

    </form>

    <br>
    <a href="/">Back to Home</a>
    """
@app.route("/appointments", methods=["GET", "POST"])
def appointments():

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        doctor = request.form["doctor"]
        appointment_date = request.form["appointment_date"]
        reason = request.form["reason"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO appointments
            (patient_id, doctor, appointment_date, reason)
            VALUES (?, ?, ?, ?)
            """,
            (patient_id, doctor, appointment_date, reason)
        )

        conn.commit()
        conn.close()

        return "<h2>Appointment booked successfully!</h2><a href='/'>Back to Home</a>"

    return """
    <h1>Book Appointment</h1>

    <form method="POST">

        <label>Patient ID:</label><br>
        <input type="number" name="patient_id"><br><br>

        <label>Doctor:</label><br>
        <input type="text" name="doctor"><br><br>

        <label>Appointment Date:</label><br>
        <input type="date" name="appointment_date"><br><br>

        <label>Reason:</label><br>
        <input type="text" name="reason"><br><br>

        <button type="submit">Book Appointment</button>

    </form>

    <br>
    <a href="/">Back to Home</a>
    """
@app.route("/prescriptions", methods=["GET", "POST"])
def prescriptions():

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        doctor = request.form["doctor"]
        medicine = request.form["medicine"]
        dosage = request.form["dosage"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO prescriptions
            (patient_id, doctor, medicine, dosage)
            VALUES (?, ?, ?, ?)
            """,
            (patient_id, doctor, medicine, dosage)
        )

        conn.commit()
        conn.close()

        return "<h2>Prescription added successfully!</h2><a href='/'>Back to Home</a>"

    return """
    <h1>Add Prescription</h1>

    <form method="POST">

        <label>Patient ID:</label><br>
        <input type="number" name="patient_id"><br><br>

        <label>Doctor:</label><br>
        <input type="text" name="doctor"><br><br>

        <label>Medicine:</label><br>
        <input type="text" name="medicine"><br><br>

        <label>Dosage:</label><br>
        <input type="text" name="dosage"><br><br>

        <button type="submit">Add Prescription</button>

    </form>

    <br>
    <a href="/">Back to Home</a>
    """
@app.route("/billing", methods=["GET", "POST"])
def billing():

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        amount = request.form["amount"]
        description = request.form["description"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO bills
            (patient_id, amount, description, status)
            VALUES (?, ?, ?, ?)
            """,
            (patient_id, amount, description, "Pending")
        )

        conn.commit()
        conn.close()

        return "<h2>Bill generated successfully!</h2><a href='/'>Back to Home</a>"

    return """
    <h1>Billing</h1>

    <form method="POST">

        <label>Patient ID:</label><br>
        <input type="number" name="patient_id"><br><br>

        <label>Amount:</label><br>
        <input type="number" step="0.01" name="amount"><br><br>

        <label>Description:</label><br>
        <input type="text" name="description"><br><br>

        <button type="submit">Generate Bill</button>

    </form>

    <br>
    <a href="/">Back to Home</a>
    """
@app.route("/medical-records", methods=["GET", "POST"])
def medical_records():

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        filename = request.form["filename"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO medical_records
            (patient_id, filename)
            VALUES (?, ?)
            """,
            (patient_id, filename)
        )

        conn.commit()
        conn.close()

        return "<h2>Medical record added successfully!</h2><a href='/'>Back to Home</a>"

    return """
    <h1>Medical Records</h1>

    <form method="POST">

        <label>Patient ID:</label><br>
        <input type="number" name="patient_id"><br><br>

        <label>Record/File Name:</label><br>
        <input type="text" name="filename"><br><br>

        <button type="submit">Add Medical Record</button>

    </form>

    <br>
    <a href="/">Back to Home</a>
    """
if __name__ == "__main__":
    app.run(debug=True)
