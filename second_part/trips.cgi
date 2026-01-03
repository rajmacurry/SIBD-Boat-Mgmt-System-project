#!/usr/bin/python3
import psycopg2
import login
import cgi

print('Content-type:text/html\n\n')
print('<html><head><title>Manage Trips</title></head><body>')
print('<h1>Manage Trips</h1>')
print('<a href="index.cgi">Back to Menu</a>')

# Form to add trip
print('<h2>Register New Trip</h2>')
print('<form action="save_trip.cgi" method="post">')
print('<p>Takeoff Date: <input type="date" name="takeoff" required/></p>')
print('<p>Arrival Date: <input type="date" name="arrival" required/></p>')
print('<p>Insurance: <input type="text" name="insurance" required/></p>')
# Origin
print('<p>From Location (Lat,Lon): <select name="from_loc">')
# Dropdown locations
connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    cursor.execute("SELECT name, latitude, longitude FROM location ORDER BY name")
    locations = cursor.fetchall()
    for loc in locations:
        val = f"{loc[1]},{loc[2]}"
        print(f'<option value="{val}">{loc[0]}</option>')
    # Reuse for To Location
    print('</select></p>')
    print('<p>To Location (Lat,Lon): <select name="to_loc">')
    for loc in locations:
        val = f"{loc[1]},{loc[2]}"
        print(f'<option value="{val}">{loc[0]}</option>')
    print('</select></p>')
    
    # Skipper validation? Should be authorised sailor. 
    # Ideally AJAX or reloading based on reservation, but for simple prototype, just list all sailors or list reservations first.
    # To register a trip, we need to know WHICH reservation it belongs to.
    # So we should pick a reservation first.
    
    print('<p>Reservation (Boat/Date): <select name="reservation_key">')
    cursor.execute("SELECT start_date, end_date, country, cni FROM reservation ORDER BY start_date DESC")
    reservations = cursor.fetchall()
    
    for res in reservations:
        # Key: start|end|country|cni
        val = f"{res[0]}|{res[1]}|{res[2]}|{res[3]}"
        label = f"{res[2]} - {res[3]} ({res[0]} to {res[1]})"
        print(f'<option value="{val}">{label}</option>')
    print('</select></p>')
    
    print('<p>Skipper Email: <input type="text" name="skipper" placeholder="Must be authorised" required/></p>')
    
    print('<input type="submit" value="Register Trip">')
    print('</form>')
    
    # List trips
    print('<h2>Existing Trips</h2>')
    cursor.execute("SELECT takeoff, arrival, boat_country, cni, skipper FROM trip ORDER BY takeoff DESC")
    print('<table border="1">')
    print('<tr><th>Takeoff</th><th>Arrival</th><th>Boat</th><th>Skipper</th></tr>')
    for row in cursor.fetchall():
        print(f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]} {row[3]}</td><td>{row[4]}</td></tr>')
    print('</table>')
    
    cursor.close()
    connection.close()
except Exception as e:
    print(f'<p>Error loading data: {e}</p>')

print('</body></html>')
