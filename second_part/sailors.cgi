#!/usr/bin/python3
import psycopg2
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Manage Sailors")

print("""
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Manage Sailors</h2>
    <a href="index.cgi" class="btn btn-secondary">← Back to Menu</a>
</div>
""")

# Form to create new sailor
print("""
<div class="card mb-5">
    <div class="card-body">
        <h4 class="card-title mb-4">Register New Sailor</h4>
        <form action="save_sailor.cgi" method="post" class="row g-3">
            <div class="col-md-6">
                <label for="firstname" class="form-label">First Name</label>
                <input type="text" class="form-control" name="firstname" id="firstname" required>
            </div>
            <div class="col-md-6">
                <label for="surname" class="form-label">Surname</label>
                <input type="text" class="form-control" name="surname" id="surname" required>
            </div>
            <div class="col-md-8">
                <label for="email" class="form-label">Email Address</label>
                <input type="email" class="form-control" name="email" id="email" required>
            </div>
            <div class="col-md-4">
                <label for="type" class="form-label">Rank</label>
                <select class="form-select" name="type" id="type">
                    <option value="junior">Junior</option>
                    <option value="senior">Senior</option>
                </select>
            </div>
            <div class="col-12 mt-4">
                <button type="submit" class="btn btn-primary w-100">Register Sailor</button>
            </div>
        </form>
    </div>
</div>
""")

# List existing sailors
print('<h4 class="mb-3">Existing Crew</h4>')
print('<div class="table-responsive">')
print('<table class="table table-striped table-hover align-middle">')
print('<thead class="table-dark"><tr><th>First Name</th><th>Surname</th><th>Email</th><th>Rank</th><th>Actions</th></tr></thead>')
print('<tbody>')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    # Selecting sailor info and determining type (Junior/Senior)
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
    
    for row in result:
        email = row[0]
        rank_badge = ""
        if row[3] == "Senior":
            rank_badge = '<span class="badge bg-warning text-dark">Senior</span>'
        elif row[3] == "Junior":
            rank_badge = '<span class="badge bg-info text-dark">Junior</span>'
        else:
            rank_badge = '<span class="badge bg-secondary">Unknown</span>'

        print('<tr>')
        print('<td>{}</td>'.format(row[1]))
        print('<td>{}</td>'.format(row[2]))
        print('<td>{}</td>'.format(email))
        print('<td>{}</td>'.format(rank_badge))
        print('<td><a href="remove_sailor.cgi?email={}" class="btn btn-danger btn-sm" onclick="return confirm(\'Are you sure you want to remove this sailor?\');">Remove</a></td>'.format(email))
        print('</tr>')
    
    cursor.close()
except Exception as e:
    print('<tr><td colspan="5" class="text-danger">Error loading sailors: {}</td></tr>'.format(e))
finally:
    if connection:
        connection.close()

print('</tbody></table>')
print('</div>')

templates.print_footer()
