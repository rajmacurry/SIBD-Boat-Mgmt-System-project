#!/usr/bin/python3
import psycopg2
import cgi
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Deleting Sailor")

form = cgi.FieldStorage()
email = form.getvalue('email')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM junior WHERE email = %s;", (email,))
    cursor.execute("DELETE FROM senior WHERE email = %s;", (email,))
    cursor.execute("DELETE FROM sailor WHERE email = %s;", (email,))
    
    connection.commit()
    print("""
    <div class="alert alert-success text-center">
        <h4>Sailor Removed</h4>
        <p>The record for <strong>{}</strong> has been deleted.</p>
        <a href="sailors.cgi" class="btn btn-outline-success">Back to List</a>
    </div>
    """.format(email))
    
except Exception as e:
    if connection:
        connection.rollback()
    print("""
    <div class="alert alert-danger">
        <h4>Deletion Failed</h4>
        <p>Error: {}</p>
        <div class="alert alert-light mt-3">
            <small>Tip: You cannot delete sailors who are currently Responsible for a Reservation or have existing Trip logs. You must delete those records first.</small>
        </div>
        <a href="sailors.cgi" class="btn btn-secondary">Back</a>
    </div>
    """.format(e))

finally:
    if connection:
        connection.close()

templates.print_footer()
