from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Hospital Management System</h1>
    <p>Welcome to the Hospital Management System.</p>

    <h3>Available Modules</h3>
    <ul>
        <li>Patient Registration</li>
        <li>Appointments</li>
        <li>Prescriptions</li>
        <li>Billing</li>
        <li>Medical Records</li>
    </ul>
    """


if __name__ == "__main__":
    app.run(debug=True)
