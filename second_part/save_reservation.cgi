#!/usr/bin/python3
import psycopg2
import cgi
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Reservation Created")

form = cgi.FieldStorage()
start_date = form.getvalue('start_date')
end_date = form.getvalue('end_date')
country = form.getvalue('country')
cni = form.getvalue('cni')
responsible = form.getvalue('responsible')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    # Needs Date Interval?
    # Check if date interval exists, if not create it
    # Note: date_interval PK is (start_date, end_date)
    cursor.execute("SELECT * FROM date_interval WHERE start_date=%s AND end_date=%s", (start_date, end_date))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO date_interval (start_date, end_date) VALUES (%s, %s)", (start_date, end_date))
    
    # Insert Reservation
    sql = """
    INSERT INTO reservation (start_date, end_date, country, cni, responsible)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (start_date, end_date, country, cni, responsible))
    
    connection.commit()
    print("""
    <div class="alert alert-success text-center">
        <h4>Reservation Confirmed!</h4>
        <p>The boat is booked from <strong>{}</strong> to <strong>{}</strong>.</p>
        <p>Responsible: <code>{}</code></p>
        <a href="reservations.cgi" class="btn btn-primary">Back to Reservations</a>
    </div>
    """.format(start_date, end_date, responsible))

except Exception as e:
    if connection:
        connection.rollback()
    
    print("""
    <div class="alert alert-danger">
        <h4>Booking Failed</h4>
        <p>Could not create reservation. Details:</p>
        <p><code>{}</code></p>
        <hr>
        <a href="reservations.cgi" class="btn btn-secondary">Try Again</a>
    </div>
    """.format(e))

finally:
    if connection:
        connection.close()

templates.print_footer()
