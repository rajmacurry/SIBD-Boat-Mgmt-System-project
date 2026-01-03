#!/usr/bin/python3
import psycopg2
import cgi
import login

print('Content-type:text/html\n\n')
print('<html><body>')

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
    print('<h3>Reservation created successfully!</h3>')
except Exception as e:
    if connection:
        connection.rollback()
    print('<h3>Error creating reservation</h3>')
    print(f'<p>{e}</p>')
finally:
    if connection:
        connection.close()

print('<p><a href="reservations.cgi">Go back</a></p>')
print('</body></html>')
