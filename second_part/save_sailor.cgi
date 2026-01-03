#!/usr/bin/python3
import psycopg2
import cgi
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<body>')

form = cgi.FieldStorage()
firstname = form.getvalue('firstname')
surname = form.getvalue('surname')
email = form.getvalue('email')
sailor_type = form.getvalue('type')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    # 1. Insert into sailor
    sql_sailor = "INSERT INTO sailor (firstname, surname, email) VALUES (%s, %s, %s);"
    cursor.execute(sql_sailor, (firstname, surname, email))
    
    # 2. Insert into specialization (junior or senior)
    if sailor_type == 'junior':
        sql_spec = "INSERT INTO junior (email) VALUES (%s);"
    elif sailor_type == 'senior':
        sql_spec = "INSERT INTO senior (email) VALUES (%s);"
    else:
        raise Exception("Invalid sailor type")
        
    cursor.execute(sql_spec, (email,))
    
    connection.commit()
    print('<h3>Sailor registered successfully!</h3>')
    print('<p><a href="sailors.cgi">Go back</a></p>')
    
    cursor.close()
except Exception as e:
    if connection:
        connection.rollback()
    print('<h3>Error registering sailor</h3>')
    print(f'<p>{e}</p>')
    print('<p><a href="sailors.cgi">Go back</a></p>')
finally:
    if connection:
        connection.close()

print('</body>')
print('</html>')
