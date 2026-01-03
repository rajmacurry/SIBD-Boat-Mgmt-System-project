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

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    # Delete reservation
    # Constraint IC-6 might make this fail if there are trips?
    # Schema says: authorised weak entity on reservation?
    # Schema: `authorised` references `reservation`.
    # So we probably need to delete from `authorised` first. 
    # And `trip` references `reservation`.
    
    # Naive delete from dependents first if not cascading:
    cursor.execute("DELETE FROM authorised WHERE start_date=%s AND end_date=%s AND boat_country=%s AND cni=%s", 
                   (start_date, end_date, country, cni))
                   
    cursor.execute("DELETE FROM trip WHERE reservation_start_date=%s AND reservation_end_date=%s AND boat_country=%s AND cni=%s", 
                   (start_date, end_date, country, cni))
    
    # Now reservation
    cursor.execute("DELETE FROM reservation WHERE start_date=%s AND end_date=%s AND country=%s AND cni=%s", 
                   (start_date, end_date, country, cni))
    
    connection.commit()
    print('<h3>Reservation removed successfully!</h3>')
except Exception as e:
    if connection:
        connection.rollback()
    print('<h3>Error removing reservation</h3>')
    print(f'<p>{e}</p>')
finally:
    if connection:
        connection.close()

print('<p><a href="reservations.cgi">Go back</a></p>')
print('</body></html>')
