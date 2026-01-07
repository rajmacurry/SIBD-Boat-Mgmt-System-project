#!/usr/bin/python3
import psycopg2
import login
import cgi
import templates
import cgitb
cgitb.enable()

templates.print_header("Manage Trips")

print("""
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Manage Trips</h2>
    <a href="index.cgi" class="btn btn-secondary">← Back to Menu</a>
</div>
""")

# Form to add trip
print("""
<div class="card mb-5">
    <div class="card-body">
        <h4 class="card-title mb-4">Log New Trip</h4>
        <form action="save_trip.cgi" method="post" class="row g-3">
            <div class="col-md-6">
                <label class="form-label">Takeoff Date</label>
                <input type="date" name="takeoff" class="form-control" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Arrival Date</label>
                <input type="date" name="arrival" class="form-control" required>
            </div>
            
            <div class="col-md-6">
                <label class="form-label">From Location</label>
                <select name="from_loc" class="form-select">
""")
# Dropdown locations
connection = None
try:
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    cursor.execute("SELECT name, latitude, longitude FROM location ORDER BY name")
    locations = cursor.fetchall()
    for loc in locations:
        val = "{},{}".format(loc[1], loc[2])
        print('<option value="{}">{}</option>'.format(val, loc[0]))
    
    print("""
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">To Location</label>
                <select name="to_loc" class="form-select">
    """)
    for loc in locations:
        val = "{},{}".format(loc[1], loc[2])
        print('<option value="{}">{}</option>'.format(val, loc[0]))
    
    print("""
                </select>
            </div>
    """)
    
    print("""
            <div class="col-md-12">
                <label class="form-label">Reservation (Boat & Date Slot)</label>
                <select name="reservation_key" class="form-select">
    """)
    
    cursor.execute("SELECT start_date, end_date, country, cni FROM reservation ORDER BY start_date DESC")
    reservations = cursor.fetchall()
    
    for res in reservations:
        # Key: start|end|country|cni
        val = "{}|{}|{}|{}".format(res[0], res[1], res[2], res[3])
        label = "{} - {} (Date: {} to {})".format(res[2], res[3], res[0], res[1])
        print('<option value="{}">{}</option>'.format(val, label))
    
    print("""
                </select>
                <div class="form-text">Choose the approved reservation for this trip.</div>
            </div>
            
            <div class="col-md-8">
                <label class="form-label">Skipper Email</label>
                <input type="text" name="skipper" class="form-control" placeholder="Must be an authorised sailor" required>
            </div>
            
             <div class="col-md-4">
                <label class="form-label">Insurance ID</label>
                <input type="text" name="insurance" class="form-control" required>
            </div>

            <div class="col-12 mt-4">
                <button type="submit" class="btn btn-primary w-100">Log Trip</button>
            </div>
        </form>
    </div>
</div>
    """)
    
    # List trips
    print('<h4 class="mb-3">Trip Logbook</h4>')
    cursor.execute("SELECT takeoff, arrival, boat_country, cni, skipper FROM trip ORDER BY takeoff DESC")
    
    print('<div class="table-responsive">')
    print('<table class="table table-striped table-hover align-middle">')
    print('<thead class="table-dark"><tr><th>Takeoff</th><th>Arrival</th><th>Boat</th><th>Skipper</th></tr></thead><tbody>')
    
    for row in cursor.fetchall():
        print('<tr>')
        print('<td>{}</td>'.format(row[0]))
        print('<td>{}</td>'.format(row[1]))
        print('<td><strong>{}</strong> <small class="text-muted">({})</small></td>'.format(row[2], row[3]))
        print('<td><code>{}</code></td>'.format(row[4]))
        print('</tr>')
    print('</tbody></table></div>')
    
    cursor.close()
    connection.close()
except Exception as e:
    print('<div class="alert alert-danger">Error loading data: {}</div>'.format(e))

templates.print_footer()
