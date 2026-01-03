#!/usr/bin/python3
import psycopg2
import cgi
import login

print('Content-type:text/html\n\n')
print('<html><body>')

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
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(sql, (takeoff, arrival, insurance, from_lat, from_lon, to_lat, to_lon, 
                         skipper, res_start_date, res_end_date, res_country, res_cni))
    
    connection.commit()
    print('<h3>Trip registered successfully!</h3>')
except Exception as e:
    if connection:
        connection.rollback()
    print('<h3>Error registering trip</h3>')
    print(f'<p>{e}</p>')
finally:
    if connection:
        connection.close()

print('<p><a href="trips.cgi">Go back</a></p>')
print('</body></html>')
