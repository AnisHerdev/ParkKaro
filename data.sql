CREATE DATABASE IF NOT EXISTS ParkKaro;
USE ParkKaro;
CREATE TABLE IF NOT EXISTS users (
                 VehicleNumber VARCHAR(20) PRIMARY KEY,
                 Password VARCHAR(20),
                 emailId VARCHAR(255),
                 ph_no INTEGER(12)
);
CREATE TABLE IF NOT EXISTS rr_nagar (
    parking_spot_id VARCHAR(10) PRIMARY KEY,
    isAvailable BOOLEAN NOT NULL
);
CREATE TABLE IF NOT EXISTS magdi_road (
    parking_spot_id VARCHAR(10) PRIMARY KEY,
    isAvailable BOOLEAN NOT NULL
);
CREATE TABLE IF NOT EXISTS pattanagere (
    parking_spot_id VARCHAR(10) PRIMARY KEY,
    isAvailable BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS all_parking_spots (
    parking_spot_id VARCHAR(10) PRIMARY KEY
);

INSERT INTO all_parking_spots (parking_spot_id)
    SELECT parking_spot_id FROM rr_nagar
    UNION
    SELECT parking_spot_id FROM magdi_road
    UNION
    SELECT parking_spot_id FROM pattanagere;


CREATE TABLE BOOKINGS(
    bookingId INTEGER PRIMARY KEY AUTO_INCREMENT,
    vehicleNumber Varchar(20) NOT NULL UNIQUE,
    parking_spot_id VARCHAR(10) NOT NULL,
    startTime timestamp default current_timestamp,
    endTime timestamp,
    duration INTEGER,

    CONSTRAINT fk_vehicleNumber
        FOREIGN KEY (vehicleNumber) REFERENCES users(VehicleNumber)
        ON DELETE CASCADE,
    CONSTRAINT fk_parkingSpot
        FOREIGN KEY (parking_spot_id) REFERENCES all_parking_spots(parking_spot_id)
        ON DELETE CASCADE
);

INSERT INTO rr_nagar (parking_spot_id, isAvailable) VALUES
('1a_RR', TRUE),
('2a_RR', FALSE),
('3a_RR', TRUE),
('4a_RR', FALSE),
('5a_RR', TRUE),
('6a_RR', FALSE),
('7a_RR', TRUE),
('8a_RR', FALSE),
('9a_RR', TRUE),
('10a_RR', FALSE),
('11a_RR', TRUE),
('12a_RR', FALSE),
('13a_RR', TRUE),
('14a_RR', FALSE),
('15a_RR', TRUE),
('16a_RR', FALSE),
('17a_RR', TRUE),
('18a_RR', FALSE),
('19a_RR', TRUE),
('20a_RR', FALSE),
('21a_RR', TRUE),
('22a_RR', FALSE),
('23a_RR', TRUE),
('24a_RR', FALSE),
('25a_RR', TRUE),
('26a_RR', FALSE),
('27a_RR', TRUE),
('28a_RR', FALSE),
('29a_RR', TRUE),
('30a_RR', FALSE);

INSERT INTO pattanagere (parking_spot_id, isAvailable) VALUES
('1a_P', FALSE),
('2a_P', TRUE),
('3a_P', FALSE),
('4a_P', TRUE),
('5a_P', FALSE),
('6a_P', TRUE),
('7a_P', FALSE),
('8a_P', TRUE),
('9a_P', FALSE),
('10a_P', TRUE),
('11a_P', FALSE),
('12a_P', TRUE),
('13a_P', FALSE),
('14a_P', TRUE),
('15a_P', FALSE),
('16a_P', TRUE),
('17a_P', FALSE),
('18a_P', TRUE),
('19a_P', FALSE),
('20a_P', TRUE),
('21a_P', FALSE),
('22a_P', TRUE),
('23a_P', FALSE),
('24a_P', TRUE),
('25a_P', FALSE),
('26a_P', TRUE),
('27a_P', FALSE),
('28a_P', TRUE),
('29a_P', FALSE),
('30a_P', TRUE);

INSERT INTO magdi_road (parking_spot_id, isAvailable) VALUES
('1a_MR', TRUE),
('2a_MR', FALSE),
('3a_MR', TRUE),
('4a_MR', FALSE),
('5a_MR', TRUE),
('6a_MR', FALSE),
('7a_MR', TRUE),
('8a_MR', FALSE),
('9a_MR', TRUE),
('10a_MR', FALSE),
('11a_MR', TRUE),
('12a_MR', FALSE),
('13a_MR', TRUE),
('14a_MR', FALSE),
('15a_MR', TRUE),
('16a_MR', FALSE),
('17a_MR', TRUE),
('18a_MR', FALSE),
('19a_MR', TRUE),
('20a_MR', FALSE),
('21a_MR', TRUE),
('22a_MR', FALSE),
('23a_MR', TRUE),
('24a_MR', FALSE),
('25a_MR', TRUE),
('26a_MR', FALSE),
('27a_MR', TRUE),
('28a_MR', FALSE),
('29a_MR', TRUE),
('30a_MR', FALSE);
