#!/usr/bin/python3
import psycopg2
import cgi
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Trip Registration")

form = cgi.FieldStorage()
takeoff = form.getvalue('takeoff')
arrival = form.getvalue('arrival')
insurance = form.getvalue('insurance')
from_loc = form.getvalue('from_loc') # "lat,lon"
to_loc = form.getvalue('to_loc') # "lat,lon"
reservation_key = form.getvalue('reservation_key') # "start|end|country|cni"
skipper = form.getvalue('skipper')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()
    
    # Parse Reservation Key
    res_parts = reservation_key.split('|')
    res_start_date = res_parts[0]
    res_end_date = res_parts[1]
    res_country = res_parts[2]
    res_cni = res_parts[3]
    
    # Parse Locations
    from_lat, from_lon = from_loc.split(',')
    to_lat, to_lon = to_loc.split(',')
    
    sql = """
    INSERT INTO trip 
    (takeoff, arrival, insurance, from_latitude, from_longitude, to_latitude, to_longitude, 
     skipper, reservation_start_date, reservation_end_date, boat_country, cni)
    VALUES (%(takeoff)s, %(arrival)s, %(insurance)s, %(from_lat)s, %(from_lon)s, %(to_lat)s, %(to_lon)s, 
     %(skipper)s, %(res_start)s, %(res_end)s, %(res_country)s, %(res_cni)s)
    """
    
    cursor.execute(sql, {'takeoff': takeoff, 'arrival': arrival, 'insurance': insurance, 
                         'from_lat': from_lat, 'from_lon': from_lon, 'to_lat': to_lat, 'to_lon': to_lon, 
                         'skipper': skipper, 'res_start': res_start_date, 'res_end': res_end_date, 
                         'res_country': res_country, 'res_cni': res_cni})
    
    connection.commit()
    print("""
    <div class="alert alert-success text-center">
        <h4>Trip Logged!</h4>
        <p>The voyage has been successfully recorded in the database.</p>
        <p>Skipper: <strong>{}</strong></p>
        <a href="trips.cgi" class="btn btn-primary">Return to Trips</a>
    </div>
    """.format(skipper))

except (Exception, psycopg2.DatabaseError) as e:
    if connection:
        connection.rollback()
    
    error_message = str(e)
    display_message = "<p><code>{}</code></p>".format(e)
    
    # Check for specific trip_check constraint violation
    if "trip_check" in error_message:
        display_message = '<p class="text-danger font-weight-bold">The sailor who is skipping is not authorised.</p>'
    
    print("""
    <div class="alert alert-danger">
        <h4>Registration Failed</h4>
        <p>There was an error logging this trip:</p>
        {}
        <hr>
        <p class="mb-0">Please check that the Skipper email is valid, authorised, and that the dates align with the reservation.</p>
        <br>
        <a href="trips.cgi" class="btn btn-secondary">Go Back</a>
    </div>
    """.format(display_message))

finally:
    if connection:
        connection.close()

templates.print_footer()
