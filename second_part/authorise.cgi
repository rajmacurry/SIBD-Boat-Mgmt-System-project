#!/usr/bin/python3
import psycopg2
import cgi
import login
import templates
import cgitb
cgitb.enable()

templates.print_header("Manage Authorizations")

form = cgi.FieldStorage()
start_date = form.getvalue('start_date')
end_date = form.getvalue('end_date')
country = form.getvalue('country')
cni = form.getvalue('cni')

# Helper to keep params passing
params = "start_date={}&end_date={}&country={}&cni={}".format(start_date, end_date, country, cni)

print("""
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Reservation Authorizations</h2>
    <a href="reservations.cgi" class="btn btn-secondary">← Back to Reservations</a>
</div>

<div class="alert alert-info">
    <strong>Reservation Context:</strong> Boat <code>{} - {}</code> from <strong>{}</strong> to <strong>{}</strong>
</div>
""".format(country, cni, start_date, end_date))

action = form.getvalue('action')
target_sailor = form.getvalue('sailor')

connection = None
try:
    connection = psycopg2.connect(login.credentials)
    connection.autocommit = False
    cursor = connection.cursor()

    # Get responsible sailor for this reservation
    cursor.execute("""
        SELECT responsible FROM reservation 
        WHERE start_date=%(start)s AND end_date=%(end)s AND country=%(country)s AND cni=%(cni)s
    """, {'start': start_date, 'end': end_date, 'country': country, 'cni': cni})
    res_row = cursor.fetchone()
    responsible_email = res_row[0] if res_row else None

    if action == 'add' and target_sailor:
        try:
            cursor.execute("""
                INSERT INTO authorised (start_date, end_date, boat_country, cni, sailor)
                VALUES (%(start)s, %(end)s, %(country)s, %(cni)s, %(sailor)s)
            """, {'start': start_date, 'end': end_date, 'country': country, 'cni': cni, 'sailor': target_sailor})
            connection.commit()
            print('<div class="alert alert-success alert-dismissible fade show">Sailor authorised successfully!<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>')
        except (Exception, psycopg2.DatabaseError) as e:
            connection.rollback()
            print('<div class="alert alert-danger alert-dismissible fade show">Error authorising: {}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>'.format(e))

    elif action == 'remove' and target_sailor:
        if target_sailor == responsible_email:
            print('<div class="alert alert-danger alert-dismissible fade show">Cannot remove the Responsible Senior from the reservation.<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>')
        else:
            try:
                cursor.execute("""
                    DELETE FROM authorised 
                    WHERE start_date=%(start)s AND end_date=%(end)s AND boat_country=%(country)s AND cni=%(cni)s AND sailor=%(sailor)s
                """, {'start': start_date, 'end': end_date, 'country': country, 'cni': cni, 'sailor': target_sailor})
                connection.commit()
                print('<div class="alert alert-warning alert-dismissible fade show">Sailor authorization revoked.<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>')
            except (Exception, psycopg2.DatabaseError) as e:
                connection.rollback()
                print('<div class="alert alert-danger alert-dismissible fade show">Error de-authorising: {}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>'.format(e))

    # 1. Dashboard Layout
    print('<div class="row g-4"><div class="col-md-7">')

    # LEFT COL: List
    print('<div class="card h-100"><div class="card-body">')
    print('<h4 class="card-title">Authorised Crew</h4>')
    
    cursor.execute("""
        SELECT s.firstname, s.surname, s.email 
        FROM authorised a
        JOIN sailor s ON a.sailor = s.email
        WHERE a.start_date=%(start)s AND a.end_date=%(end)s AND a.boat_country=%(country)s AND a.cni=%(cni)s
    """, {'start': start_date, 'end': end_date, 'country': country, 'cni': cni})
    
    print('<ul class="list-group list-group-flush mt-3">')
    results = cursor.fetchall()
    if not results:
        print('<li class="list-group-item text-muted">No sailors authorised yet.</li>')
    
    for row in results:
        is_responsible = (row[2] == responsible_email)
        
        print("""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <div>
                <strong>{} {}</strong> {}
                <br><small class="text-muted">{}</small>
            </div>
            {}
        </li>
        """.format(
            row[0], row[1], 
            '<span class="badge bg-primary ms-2">Responsible</span>' if is_responsible else '',
            row[2],
            '<span class="text-muted fst-italic small">Cannot Remove</span>' if is_responsible else '<a href="authorise.cgi?{}&action=remove&sailor={}" class="btn btn-sm btn-outline-danger">Revoke</a>'.format(params, row[2])
        ))
    print('</ul>')
    print('</div></div></div>') # End col, card, body

    # RIGHT COL: Add Form
    print('<div class="col-md-5">')
    print('<div class="card h-100"><div class="card-body bg-light">')
    print('<h4 class="card-title">Authorise New Sailor</h4>')
    print('<p class="card-text text-muted">Grant access to this reservation.</p>')
    
    print('<form action="authorise.cgi" method="get">') 
    # Hidden Inputs
    print('<input type="hidden" name="start_date" value="{}">'.format(start_date))
    print('<input type="hidden" name="end_date" value="{}">'.format(end_date))
    print('<input type="hidden" name="country" value="{}">'.format(country))
    print('<input type="hidden" name="cni" value="{}">'.format(cni))
    print('<input type="hidden" name="action" value="add">')
    
    print('<div class="mb-3"><label class="form-label">Select Sailor</label>')
    print('<select name="sailor" class="form-select" size="10">')
    
    cursor.execute("SELECT email, firstname, surname FROM sailor ORDER BY firstname")
    for s_row in cursor.fetchall():
        print('<option value="{}">{} {} ({})</option>'.format(s_row[0], s_row[1], s_row[2], s_row[0]))
    
    print('</select></div>')
    print('<button type="submit" class="btn btn-success w-100">Grant Authorization</button>')
    print('</form>')
    
    print('</div></div></div></div>') # End card, col, row

    cursor.close()
    connection.close()

except Exception as e:
    print('<div class="alert alert-danger">Error: {}</div>'.format(e))

templates.print_footer()
