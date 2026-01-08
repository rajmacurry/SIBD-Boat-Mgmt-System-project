#!/usr/bin/python3
import psycopg2
import cgi
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Deleting Trip")

form = cgi.FieldStorage()
takeoff = form.getvalue('takeoff')
res_start = form.getvalue('res_start')
res_end = form.getvalue('res_end')
country = form.getvalue('country')
cni = form.getvalue('cni')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()
    
    sql = """
    DELETE FROM trip 
    WHERE takeoff = %(takeoff)s 
    AND reservation_start_date = %(res_start)s 
    AND reservation_end_date = %(res_end)s 
    AND boat_country = %(country)s 
    AND cni = %(cni)s
    """
    
    params = {
        'takeoff': takeoff,
        'res_start': res_start,
        'res_end': res_end,
        'country': country,
        'cni': cni
    }
    
    cursor.execute(sql, params)
    
    connection.commit()
    
    print("""
    <div class="alert alert-success text-center">
        <h4>Trip Deleted</h4>
        <p>The trip record has been successfully removed.</p>
        <a href="trips.cgi" class="btn btn-outline-success">Return to Logbook</a>
    </div>
    """)
    
except (Exception, psycopg2.DatabaseError) as e:
    if connection:
        connection.rollback()
    print("""
    <div class="alert alert-danger">
        <h4>Deletion Failed</h4>
        <p>Error: {}</p>
        <a href="trips.cgi" class="btn btn-secondary">Back</a>
    </div>
    """.format(e))

finally:
    if connection:
        connection.close()

templates.print_footer()
