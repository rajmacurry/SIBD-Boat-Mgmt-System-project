#!/usr/bin/python3
import psycopg2
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Manage Reservations")

print("""
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Manage Reservations</h2>
    <a href="index.cgi" class="btn btn-secondary">← Back to Menu</a>
</div>
""")

# Form to create new reservation
print("""
<div class="card mb-5">
    <div class="card-body">
        <h4 class="card-title mb-4">Book a Boat</h4>
        <form action="save_reservation.cgi" method="post" class="row g-3">
            <div class="col-md-6">
                <label class="form-label">Start Date</label>
                <input type="date" name="start_date" class="form-control" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">End Date</label>
                <input type="date" name="end_date" class="form-control" required>
            </div>
            
            <div class="col-md-6">
                <label class="form-label">Boat Country</label>
                <input type="text" name="country" class="form-control" placeholder="e.g. PRT" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Boat CNI</label>
                <input type="text" name="cni" class="form-control" placeholder="Boat Identifier" required>
            </div>
            
            <div class="col-md-12">
                <label class="form-label">Responsible Senior</label>
                <select name="responsible" class="form-select">
""")

try:
    conn = psycopg2.connect(login.credentials)
    cur = conn.cursor()
    cur.execute("SELECT s.email, s.firstname, s.surname FROM senior sn JOIN sailor s ON sn.email = s.email;")
    for row in cur.fetchall():
        print('<option value="{}">{} {} ({})</option>'.format(row[0], row[1], row[2], row[0]))
    cur.close()
    conn.close()
except:
    print('<option>Error loading seniors - Check DB Connection</option>')

print("""
                </select>
                <div class="form-text">Only Senior sailors can be responsible for a reservation.</div>
            </div>
            
            <div class="col-12 mt-4">
                <button type="submit" class="btn btn-primary w-100">Make Reservation</button>
            </div>
        </form>
    </div>
</div>
""")

# List existing reservations
print('<h4 class="mb-3">Current Reservations</h4>')
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
    
    print('<div class="table-responsive">')
    print('<table class="table table-striped table-hover align-middle">')
    print('<thead class="table-dark"><tr><th>Start</th><th>End</th><th>Boat</th><th>Responsible</th><th>Actions</th></tr></thead>')
    print('<tbody>')
    
    for row in results:
        # Construct composite key for deletion
        params = "start_date={}&end_date={}&country={}&cni={}".format(row[0], row[1], row[2], row[3])
        print('<tr>')
        print('<td>{}</td>'.format(row[0]))
        print('<td>{}</td>'.format(row[1]))
        print('<td><div><strong>{}</strong></div><small class="text-muted">{}</small></td>'.format(row[2], row[3]))
        print('<td><small>{}</small></td>'.format(row[4]))
        print('<td>')
        print('<div class="btn-group" role="group">')
        print('<a href="authorise.cgi?{}" class="btn btn-sm btn-outline-primary">Auths</a>'.format(params))
        print('<a href="remove_reservation.cgi?{}" onclick="return confirm(\'Delete reservation?\');" class="btn btn-sm btn-outline-danger">Delete</a>'.format(params))
        print('</div>')
        print('</td>')
        print('</tr>')
    print('</tbody></table></div>')
    
    cur.close()
    conn.close()
except Exception as e:
    print('<div class="alert alert-danger">Error: {}</div>'.format(e))

templates.print_footer()
