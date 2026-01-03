#!/usr/bin/python3
import psycopg2
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Manage Sailors</title>')
print('</head>')
print('<body>')
print('<h1>Manage Sailors</h1>')
print('<a href="index.cgi">Back to Menu</a>')

# Form to create new sailor
print('<h2>Register New Sailor</h2>')
print('<form action="save_sailor.cgi" method="post">')
print('<p>First Name: <input type="text" name="firstname" required/></p>')
print('<p>Surname: <input type="text" name="surname" required/></p>')
print('<p>Email: <input type="email" name="email" required/></p>')
print('<p>Type: ')
print('<select name="type">')
print('<option value="junior">Junior</option>')
print('<option value="senior">Senior</option>')
print('</select>')
print('</p>')
print('<p><input type="submit" value="Register Sailor"/></p>')
print('</form>')

# List existing sailors
print('<h2>Existing Sailors</h2>')
connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    # Selecting sailor info and determining type (Junior/Senior)
    # Using LEFT JOINs to check existence in sub-tables
    sql = """
    SELECT s.email, s.firstname, s.surname, 
           CASE WHEN j.email IS NOT NULL THEN 'Junior' 
                WHEN sn.email IS NOT NULL THEN 'Senior' 
                ELSE 'Unknown' END as type
    FROM sailor s
    LEFT JOIN junior j ON s.email = j.email
    LEFT JOIN senior sn ON s.email = sn.email
    ORDER BY s.firstname;
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    
    print('<table border="1" cellspacing="0" cellpadding="5">')
    print('<tr><th>First Name</th><th>Surname</th><th>Email</th><th>Type</th><th>Actions</th></tr>')
    for row in result:
        email = row[0]
        print('<tr>')
        print(f'<td>{row[1]}</td>') # Firstname
        print(f'<td>{row[2]}</td>') # Surname
        print(f'<td>{email}</td>')   # Email
        print(f'<td>{row[3]}</td>') # Type
        print(f'<td><a href="remove_sailor.cgi?email={email}" onclick="return confirm(\'Are you sure?\');">Remove</a></td>')
        print('</tr>')
    print('</table>')
    
    cursor.close()
except Exception as e:
    print(f'<p style="color:red">Error: {e}</p>')
finally:
    if connection:
        connection.close()

print('</body>')
print('</html>')
