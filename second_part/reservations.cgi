#!/usr/bin/python3
import psycopg2
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head><title>Manage Reservations</title></head>')
print('<body>')
print('<h1>Manage Reservations</h1>')
print('<a href="index.cgi">Back to Menu</a>')

# Form to create new reservation
print('<h2>Create Reservation</h2>')
print('<form action="save_reservation.cgi" method="post">')
print('<p>Start Date (YYYY-MM-DD): <input type="date" name="start_date" required/></p>')
print('<p>End Date (YYYY-MM-DD): <input type="date" name="end_date" required/></p>')
print('<p>Country: <input type="text" name="country" required/></p>')
print('<p>CNI: <input type="text" name="cni" required/></p>')
print('<p>Responsible Senior Email: <select name="responsible">')
# Dropdown for Seniors
try:
    conn = psycopg2.connect(login.credentials)
    cur = conn.cursor()
    cur.execute("SELECT s.email, s.firstname, s.surname FROM senior sn JOIN sailor s ON sn.email = s.email;")
    for row in cur.fetchall():
        print(f'<option value="{row[0]}">{row[1]} {row[2]} ({row[0]})</option>')
    cur.close()
    conn.close()
except:
    print('<option>Error loading seniors</option>')
print('</select></p>')
print('<p><input type="submit" value="Create Reservation"/></p>')
print('</form>')

# List existing reservations
print('<h2>Existing Reservations</h2>')
try:
    conn = psycopg2.connect(login.credentials)
    cur = conn.cursor()
    sql = """
    SELECT start_date, end_date, country, cni, responsible 
    FROM reservation
    ORDER BY start_date DESC;
    """
    cur.execute(sql)
    results = cur.fetchall()
    
    print('<table border="1" cellpadding="5">')
    print('<tr><th>Start</th><th>End</th><th>Country</th><th>CNI</th><th>Responsible</th><th>Actions</th></tr>')
    for row in results:
        # Construct composite key for deletion
        # Passing multiple params
        params = f"start_date={row[0]}&end_date={row[1]}&country={row[2]}&cni={row[3]}"
        print('<tr>')
        print(f'<td>{row[0]}</td>')
        print(f'<td>{row[1]}</td>')
        print(f'<td>{row[2]}</td>')
        print(f'<td>{row[3]}</td>')
        print(f'<td>{row[4]}</td>')
        print(f'<td>')
        print(f'<a href="remove_reservation.cgi?{params}" onclick="return confirm(\'Delete reservation?\');">Remove</a> | ')
        print(f'<a href="authorise.cgi?{params}">Manage Auth</a>')
        print('</td>')
        print('</tr>')
    print('</table>')
    cur.close()
    conn.close()
except Exception as e:
    print(f'<p>Error: {e}</p>')

print('</body></html>')
