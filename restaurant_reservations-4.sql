-- Drop and create the database
DROP DATABASE IF EXISTS restaurant_reservations;
CREATE DATABASE restaurant_reservations;
USE restaurant_reservations;

-- Create customers table
CREATE TABLE customers (
    customerId INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    customerName VARCHAR(45) NOT NULL,
    contactInfo VARCHAR(200)
);

-- Create reservations table
CREATE TABLE reservations (
    reservationId INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    customerId INT,
    reservationTime DATETIME NOT NULL,
    numberOfGuests INT NOT NULL,
    specialRequests VARCHAR(200),
    FOREIGN KEY (customerId) REFERENCES customers(customerId)
);

-- Create diningPreferences table
CREATE TABLE diningPreferences (
    preferenceId INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    customerId INT,
    favoriteTable VARCHAR(45),
    dietaryRestrictions VARCHAR(200),
    FOREIGN KEY (customerId) REFERENCES customers(customerId)
);

-- Insert initial values into customers table
INSERT INTO customers(customerName, contactInfo) VALUES
('Victor', 'VictorDCastillo@example.com'),
('Isis', 'Isisa@example.com'),
('Kassandra', 'KO@example.com'),
('Bobby Jones', 'bobbJ@example.com'),
('Jaylen', 'Jaylen@example.com');

-- Insert initial values into reservations table
INSERT INTO reservations(customerId, reservationTime, numberOfGuests, specialRequests) VALUES
(1, '2024-05-20 19:00:00', 2, 'Window seat preferred'),
(2, '2024-05-21 20:00:00', 4, 'Allergic to peanuts'),
(3, '2024-05-22 18:30:00', 3, 'Celebrating anniversary'),
(4, '2024-05-23 19:45:00', 5, 'Need high chair for a toddler'),
(5, '2024-05-24 20:30:00', 2, 'Vegetarian meal options');

-- Insert initial values into diningPreferences table
INSERT INTO diningPreferences(customerId, favoriteTable, dietaryRestrictions) VALUES
(1, 'Table 5', 'None'),
(2, 'Table 9', 'Gluten-free'),
(3, 'Table 20', 'Vegetarian'),
(4, 'Table 15', 'No dairy'),
(5, 'Table 1', 'Vegan');

-- Procedure to find all reservations for a customer using their ID
DELIMITER //
CREATE PROCEDURE findReservations(IN in_customerId INT)
BEGIN
    SELECT * FROM reservations WHERE customerId = in_customerId;
END //
DELIMITER ;

-- Procedure to update the specialRequests field in the reservations table
DELIMITER $$
CREATE PROCEDURE addSpecialRequest(IN in_reservationId INT, IN in_requests VARCHAR(200))
BEGIN
    UPDATE reservations SET specialRequests = in_requests WHERE reservationId = in_reservationId;
END $$
DELIMITER ;

-- Procedure to create a new reservation with customer details
DELIMITER $$
CREATE PROCEDURE addReservation(
    IN in_customerName VARCHAR(45), 
    IN in_contactInfo VARCHAR(200), 
    IN in_reservationTime DATETIME, 
    IN in_numberOfGuests INT, 
    IN in_specialRequests VARCHAR(200)
)
BEGIN
    DECLARE customerId INT;
    DECLARE count INT;
    
    -- Check if customer name and contact info are provided
    IF in_customerName IS NULL OR in_contactInfo IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Customer name and contact info are required.';
    END IF;
    
    -- Check if reservation time is in the future
    IF in_reservationTime <= NOW() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Reservation time must be in the future.';
    END IF;
    
    -- Check if number of guests is valid
    IF in_numberOfGuests <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Number of guests must be a positive integer.';
    END IF;
    
    -- Check if customer already exists
    SELECT COUNT(*) INTO count FROM customers 
    WHERE customerName = in_customerName AND contactInfo = in_contactInfo;
    
    IF count = 0 THEN
        -- If customer does not exist, create a new one
        INSERT INTO customers (customerName, contactInfo) VALUES (in_customerName, in_contactInfo);
        SET customerId = LAST_INSERT_ID();
    ELSE
        -- If customer already exists, retrieve their ID
        SELECT customerId INTO customerId FROM customers 
        WHERE customerName = in_customerName AND contactInfo = in_contactInfo;
    END IF;
    
    -- Add reservation
    INSERT INTO reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES
    (customerId, in_reservationTime, in_numberOfGuests, in_specialRequests);
    
    -- Procedure to delete a reservation by reservationId
DELIMITER $$
CREATE PROCEDURE deleteReservation(IN in_reservationId INT)
BEGIN
    DELETE FROM reservations WHERE reservationId = in_reservationId;
END $$
DELIMITER ;

-- Call the deleteReservation procedure to delete a reservation
CALL deleteReservation(1); -- Assuming reservationId 1 is the reservation you want to delete

-- Check if the reservation was deleted
SELECT * FROM reservations;

END $$
DELIMITER ;