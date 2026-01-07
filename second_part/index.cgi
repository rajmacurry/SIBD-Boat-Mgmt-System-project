#!/usr/bin/python3
import templates
import cgitb
cgitb.enable()

templates.print_header("Sailing Project - Main Menu")

print("""
<div class="text-center mb-5">
    <h1 class="display-4 text-primary fw-bold">⚓ Sailing Manager</h1>
    <p class="lead text-muted">Manage your fleet, crew, and adventures</p>
</div>

<div class="row g-4 justify-content-center">
    <div class="col-md-4">
        <a href="sailors.cgi" class="menu-link">
            <div class="mb-2">👨‍✈️</div>
            Manage Sailors
        </a>
    </div>
    <div class="col-md-4">
        <a href="reservations.cgi" class="menu-link">
            <div class="mb-2">📅</div>
            Manage Reservations
        </a>
    </div>
    <div class="col-md-4">
        <a href="trips.cgi" class="menu-link">
             <div class="mb-2">⛵</div>
            Manage Trips
        </a>
    </div>
</div>

<div class="text-center mt-5">
    <small class="text-muted">SIBD Project Part 2</small>
</div>
""")

templates.print_footer()
