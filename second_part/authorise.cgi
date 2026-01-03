#!/usr/bin/python3
import psycopg2
import cgi
import login

print('Content-type:text/html\n\n')
print('<html><head><title>Manage Authorizations</title></head><body>')

form = cgi.FieldStorage()
start_date = form.getvalue('start_date')
end_date = form.getvalue('end_date')
country = form.getvalue('country')
cni = form.getvalue('cni')

# Helper to keep params passing
params = f"start_date={start_date}&end_date={end_date}&country={country}&cni={cni}"

print(f'<h1>Authorizations for Reservation</h1>')
print(f'<p><b>Reservation:</b> {country} / {cni} ({start_date} to {end_date})</p>')
print(f'<a href="reservations.cgi">Back to Reservations</a>')

# Handle Add/Remove POST actions within this script for simplicity, or simpler: show form and utilize separate action script
# But to show the list, we need this page.
# Let's check if we have an action
action = form.getvalue('action')
target_sailor = form.getvalue('sailor')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()

    if action == 'add' and target_sailor:
        try:
            cursor.execute("""
                INSERT INTO authorised (start_date, end_date, boat_country, cni, sailor)
                VALUES (%s, %s, %s, %s, %s)
            """, (start_date, end_date, country, cni, target_sailor))
            connection.commit()
            print('<p style="color:green">Sailor authorised!</p>')
        except Exception as e:
            connection.rollback()
            print(f'<p style="color:red">Error authorising: {e}</p>')

    elif action == 'remove' and target_sailor:
        try:
            cursor.execute("""
                DELETE FROM authorised 
                WHERE start_date=%s AND end_date=%s AND boat_country=%s AND cni=%s AND sailor=%s
            """, (start_date, end_date, country, cni, target_sailor))
            connection.commit()
            print('<p style="color:green">Sailor de-authorised!</p>')
        except Exception as e:
            connection.rollback()
            print(f'<p style="color:red">Error de-authorising: {e}</p>')

    # 1. List currently authorised sailors
    print('<h3>Authorised Sailors</h3>')
    cursor.execute("""
        SELECT s.firstname, s.surname, s.email 
        FROM authorised a
        JOIN sailor s ON a.sailor = s.email
        WHERE a.start_date=%s AND a.end_date=%s AND a.boat_country=%s AND a.cni=%s
    """, (start_date, end_date, country, cni))
    
    print('<ul>')
    for row in cursor.fetchall():
        print(f'<li>{row[0]} {row[1]} ({row[2]}) '
              f'[<a href="authorise.cgi?{params}&action=remove&sailor={row[2]}">Revoke</a>]</li>')
    print('</ul>')

    # 2. Form to add new sailor
    print('<h3>Authorise New Sailor</h3>')
    # Get all sailors NOT authorised needed? Or just all sailors?
    # Just a simple dropdown of all sailors is easier for prototype.
    cursor.execute("SELECT email, firstname, surname FROM sailor ORDER BY firstname")
    
    print(f'<form action="authorise.cgi" method="get">') # Using GET to keep state easily in URL or POST? 
    # If GET, all params need to be hidden inputs.
    print(f'<input type="hidden" name="start_date" value="{start_date}">')
    print(f'<input type="hidden" name="end_date" value="{end_date}">')
    print(f'<input type="hidden" name="country" value="{country}">')
    print(f'<input type="hidden" name="cni" value="{cni}">')
    print(f'<input type="hidden" name="action" value="add">')
    
    print('Sailor: <select name="sailor">')
    for s_row in cursor.fetchall():
        print(f'<option value="{s_row[0]}">{s_row[1]} {s_row[2]} ({s_row[0]})</option>')
    print('</select>')
    print('<input type="submit" value="Authorise">')
    print('</form>')

    cursor.close()
    connection.close()

except Exception as e:
    print(f'<p>Error: {e}</p>')

print('</body></html>')
