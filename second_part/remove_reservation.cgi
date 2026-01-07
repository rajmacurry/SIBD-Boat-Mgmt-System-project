#!/usr/bin/python3
import psycopg2
import cgi
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Reservation Removal")

form = cgi.FieldStorage()
start_date = form.getvalue('start_date')
end_date = form.getvalue('end_date')
country = form.getvalue('country')
cni = form.getvalue('cni')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    # Delete dependent data first
    cursor.execute("DELETE FROM authorised WHERE start_date=%s AND end_date=%s AND boat_country=%s AND cni=%s", 
                   (start_date, end_date, country, cni))
                   
    cursor.execute("DELETE FROM trip WHERE reservation_start_date=%s AND reservation_end_date=%s AND boat_country=%s AND cni=%s", 
                   (start_date, end_date, country, cni))
    
    # Now reservation
    cursor.execute("DELETE FROM reservation WHERE start_date=%s AND end_date=%s AND country=%s AND cni=%s", 
                   (start_date, end_date, country, cni))
    
    connection.commit()
    print("""
    <div class="alert alert-success text-center">
        <h4>Reservation Deleted</h4>
        <p>The booking and all associated authorisations/trips have been removed.</p>
        <a href="reservations.cgi" class="btn btn-outline-success">Return to List</a>
    </div>
    """)
    
except Exception as e:
    if connection:
        connection.rollback()
    
    print("""
    <div class="alert alert-danger">
        <h4>Deletion Failed</h4>
        <p>Error: {}</p>
        <a href="reservations.cgi" class="btn btn-secondary">Back</a>
    </div>
    """.format(e))

finally:
    if connection:
        connection.close()

templates.print_footer()
