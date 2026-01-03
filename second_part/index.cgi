#!/usr/bin/python3
import cgi

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Sailing Project Application</title>')
print('</head>')
print('<body>')
print('<h1>Sailing Project - Part 5</h1>')
print('<h2>Main Menu</h2>')
print('<ul>')
print('<li><a href="sailors.cgi">Manage Sailors</a></li>')
print('<li><a href="reservations.cgi">Manage Reservations</a></li>')
print('<li><a href="trips.cgi">Manage Trips</a></li>')
# print('<li><a href="authorise.cgi">Manage Authorizations</a></li>')
print('</ul>')
print('</body>')
print('</html>')
