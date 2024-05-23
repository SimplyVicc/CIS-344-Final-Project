from http.server import HTTPServer, BaseHTTPRequestHandler
from restaurantDatabase import RestaurantDatabase
import cgi

class RestaurantPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        self.database = RestaurantDatabase()
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        if self.path == '/addReservation':
            try:
                # Process the form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_id = int(form.getvalue("customer_id"))
                reservation_time = form.getvalue("reservation_time")
                number_of_guests = int(form.getvalue("number_of_guests"))
                special_requests = form.getvalue("special_requests") or ""

                # Call the Database Method to add a new reservation
                try:
                    self.database.addReservation(customer_id, reservation_time, number_of_guests, special_requests)
                    print("Reservation added for customer ID:", customer_id)

                    # Respond with a confirmation message
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    self.wfile.write(b"<html><head><title>Add Reservation</title></head>")
                    self.wfile.write(b"<body>")
                    self.wfile.write(b"<center><h2>Reservation Added</h2>")
                    self.wfile.write(b"<p>Reservation has been successfully added.</p>")
                    self.wfile.write(b"<a href='/addReservation'>Add Another Reservation</a><br>")
                    self.wfile.write(b"<a href='/viewReservations'>View Reservations</a></center>")
                    self.wfile.write(b"</body></html>")
                except Exception as e:
                    # Handle specific database errors
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    self.wfile.write(b"<html><head><title>Error</title></head>")
                    self.wfile.write(b"<body>")
                    self.wfile.write(b"<center><h2>Error Adding Reservation</h2>")
                    self.wfile.write(b"<p>")
                    self.wfile.write(str(e).encode())
                    self.wfile.write(b"</p>")
                    self.wfile.write(b"<a href='/addReservation'>Try Again</a><br>")
                    self.wfile.write(b"<a href='/viewReservations'>View Reservations</a></center>")
                    self.wfile.write(b"</body></html>")
                    
            except Exception as e:
                self.send_error(500, 'Server Error: %s' % str(e))

    def do_GET(self):
        try:
            if self.path == '/':
                self.show_home_page()
                return

            if self.path == '/addReservation':
                self.show_add_reservation_form()
                return

            if self.path == '/viewReservations':
                self.show_view_reservations()
                return
            
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
    
    def show_home_page(self):
        records = self.database.getAllReservations()
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div> <a href='/'>Home</a>| \
                         <a href='/addReservation'>Add Reservation</a>|\
                          <a href='/viewReservations'>View Reservations</a></div>")
        self.wfile.write(b"<hr><h2>All Reservations</h2>")
        self.wfile.write(b"<table border=2> \
                            <tr><th> Reservation ID </th>\
                                <th> Customer ID </th>\
                                <th> Reservation Time </th>\
                                <th> Number of Guests </th>\
                                <th> Special Requests </th></tr>")
        for row in records:
            self.wfile.write(b' <tr> <td>')
            self.wfile.write(str(row[0]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[1]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[2]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[3]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[4]).encode())
            self.wfile.write(b'</td></tr>')
        
        self.wfile.write(b"</table></center>")
        self.wfile.write(b"</body></html>")
    
    def show_add_reservation_form(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(b"<html><head><title>Add Reservation</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h2>Add Reservation</h2>")
        self.wfile.write(b"<form method='post' action='/addReservation'>")
        self.wfile.write(b"<label>Customer ID: </label>")
        self.wfile.write(b"<input type='text' name='customer_id'><br>")
        self.wfile.write(b"<label>Reservation Time: </label>")
        self.wfile.write(b"<input type='text' name='reservation_time'><br>")
        self.wfile.write(b"<label>Number of Guests: </label>")
        self.wfile.write(b"<input type='text' name='number_of_guests'><br>")
        self.wfile.write(b"<label>Special Requests: </label>")
        self.wfile.write(b"<input type='text' name='special_requests'><br>")
        self.wfile.write(b"<input type='submit' value='Submit'>")
        self.wfile.write(b"</form>")
        self.wfile.write(b"</center></body></html>")
    
    def show_view_reservations(self):
        reservations = self.database.getAllReservations()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        self.wfile.write(b"<html><head><title>View Reservations</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h2>All Reservations</h2>")
        self.wfile.write(b"<table border=1>")
        self.wfile.write(b"<tr><th>Reservation ID</th><th>Customer ID</th><th>Reservation Time</th><th>Number of Guests</th><th>Special Requests</th></tr>")
        
        for row in reservations:
            self.wfile.write(b"<tr>")
            for item in row:
                self.wfile.write(b"<td>")
                self.wfile.write(str(item).encode())
                self.wfile.write(b"</td>")
            self.wfile.write(b"</tr>")
            
        self.wfile.write(b"</table>")
        self.wfile.write(b"</center></body></html>")

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()
