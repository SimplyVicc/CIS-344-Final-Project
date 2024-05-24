import mysql.connector
from mysql.connector import Error

class restaurantDatabase:
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="restaurant_reservations",
                 user='root',
                 password='Yankees249967'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def addReservation(self, name, contact_info, reservation_time, number_of_guests, special_requests):
        ''' Method to insert a new reservation using the stored procedure '''
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                # Prepare the call to the stored procedure
                args = [name, contact_info, reservation_time, number_of_guests, special_requests]
                cursor.callproc('addReservation', args)
                
                self.connection.commit()
                print("Reservation added successfully")
            except Error as e:
                self.connection.rollback()
                print("Failed to add reservation:", e)
                raise e
            finally:
                cursor.close()

    def getAllReservations(self):
        ''' Method to get all reservations from the reservations table '''
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM reservations"
                cursor.execute(query)
                records = cursor.fetchall()
                return records
            except Error as e:
                print("Failed to retrieve reservations:", e)
            finally:
                cursor.close()

    def addCustomer(self, customer_name, contact_info):
        ''' Method to add a new customer to the customers table '''
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                query = "INSERT INTO customers (customerName, contactInfo) VALUES (%s, %s)"
                cursor.execute(query, (customer_name, contact_info))
                self.connection.commit()
                print("Customer added successfully")
            except Error as e:
                self.connection.rollback()
                print("Failed to add customer:", e)
                raise e
            finally:
                cursor.close()

    def getCustomerPreferences(self, customer_id):
        ''' Method to retrieve dining preferences for a specific customer '''
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM diningPreferences WHERE customerId = %s"
                cursor.execute(query, (customer_id,))
                preferences = cursor.fetchall()
                return preferences
            except Error as e:
                print("Failed to retrieve customer preferences:", e)
            finally:
                cursor.close()

    # Add more methods as needed for restaurant operations
