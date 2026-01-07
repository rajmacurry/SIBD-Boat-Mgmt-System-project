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
    connection.autocommit = False
    cursor = connection.cursor()
    
    # Delete dependent data first
    params = {'start': start_date, 'end': end_date, 'country': country, 'cni': cni}
    
    cursor.execute("DELETE FROM authorised WHERE start_date=%(start)s AND end_date=%(end)s AND boat_country=%(country)s AND cni=%(cni)s", 
                   params)
                   
    cursor.execute("DELETE FROM trip WHERE reservation_start_date=%(start)s AND reservation_end_date=%(end)s AND boat_country=%(country)s AND cni=%(cni)s", 
                   params)
    
    # Now reservation
    cursor.execute("DELETE FROM reservation WHERE start_date=%(start)s AND end_date=%(end)s AND country=%(country)s AND cni=%(cni)s", 
                   params)
    
    connection.commit()
    print("""
    <div class="alert alert-success text-center">
        <h4>Reservation Deleted</h4>
        <p>The booking and all associated authorisations/trips have been removed.</p>
        <a href="reservations.cgi" class="btn btn-outline-success">Return to List</a>
    </div>
    """)
    
except (Exception, psycopg2.DatabaseError) as e:
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
