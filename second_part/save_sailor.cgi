#!/usr/bin/python3
import psycopg2
import cgi
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Sailor Registration")

form = cgi.FieldStorage()
firstname = form.getvalue('firstname')
surname = form.getvalue('surname')
email = form.getvalue('email')
sailor_type = form.getvalue('type')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()
    
    # Defer constraints to ensure mandatory specialization check waits until both inserts are done
    cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
    
# 2. Insert into specialization
    if sailor_type == 'junior':
        sql_spec = "INSERT INTO junior (email) VALUES (%(email)s);"
    elif sailor_type == 'senior':
        sql_spec = "INSERT INTO senior (email) VALUES (%(email)s);"
    else:
        raise Exception("Invalid sailor type")

    # 1. Insert into sailor
    sql_sailor = "INSERT INTO sailor (firstname, surname, email) VALUES (%(firstname)s, %(surname)s, %(email)s);"
    cursor.execute(sql_sailor, {'firstname': firstname, 'surname': surname, 'email': email})
    
    
        
    cursor.execute(sql_spec, {'email': email})
    
    connection.commit()
    
    print("""
    <div class="alert alert-success text-center" role="alert">
        <h4 class="alert-heading">Success!</h4>
        <p>Sailor <strong>{} {}</strong> registered successfully.</p>
        <hr>
        <p class="mb-0"><a href="sailors.cgi" class="btn btn-primary">Return to Sailors List</a></p>
    </div>
    """.format(firstname, surname))
    
    cursor.close()
except (Exception, psycopg2.DatabaseError) as e:
    if connection:
        connection.rollback()
    
    print("""
    <div class="alert alert-danger" role="alert">
        <h4 class="alert-heading">Registration Failed</h4>
        <p>Could not register sailor. Determining the cause:</p>
        <p><code>{}</code></p>
        <hr>
        <p class="mb-0"><a href="sailors.cgi" class="btn btn-secondary">Try Again</a></p>
    </div>
    """.format(e))
    
finally:
    if connection:
        connection.close()

templates.print_footer()
