-- SET search_path TO project;


-- Drop all tables

DROP TABLE IF EXISTS acquires CASCADE;
DROP TABLE IF EXISTS Certification CASCADE;
DROP TABLE IF EXISTS belongs_to CASCADE;
DROP TABLE IF EXISTS Trip CASCADE;
DROP TABLE IF EXISTS lists CASCADE;
DROP TABLE IF EXISTS defines CASCADE;
DROP TABLE IF EXISTS Location CASCADE;
DROP TABLE IF EXISTS is_responsible CASCADE;
DROP TABLE IF EXISTS reserves CASCADE;
DROP TABLE IF EXISTS Reservation CASCADE;
DROP TABLE IF EXISTS Junior CASCADE;
DROP TABLE IF EXISTS Senior CASCADE;
DROP TABLE IF EXISTS Sailor CASCADE;
DROP TABLE IF EXISTS National CASCADE;
DROP TABLE IF EXISTS International CASCADE;
DROP TABLE IF EXISTS Jurisdictions CASCADE;
DROP TABLE IF EXISTS Class CASCADE;
DROP TABLE IF EXISTS Boat CASCADE;
DROP TABLE IF EXISTS Country CASCADE;



-- Creating the Country
CREATE TABLE Country(
    iso VARCHAR(3),
    flag VARCHAR(2083) NOT NULL, --IC8
    name VARCHAR(70) NOT NULL, -- IC8
    PRIMARY KEY (iso),
    UNIQUE (name),
    UNIQUE (flag)

);

CREATE TABLE Class(
    class_name VARCHAR(80),
    max_len INTEGER NOT NULL,
    PRIMARY KEY (class_name),
    CHECK (max_len > 0)
);

CREATE TABLE Boat(
    country_iso VARCHAR(3) NOT NULL,
    boat_name VARCHAR(80) NOT NULL,
    len INTEGER NOT NULL,
    cni INTEGER NOT NULL,
    year INTEGER NOT NULL,
    image VARCHAR(2083) NOT NULL,
    class_name VARCHAR(80),
    PRIMARY KEY (country_iso, cni),
    FOREIGN KEY (country_iso) REFERENCES Country(iso),
    FOREIGN KEY (class_name) REFERENCES Class(class_name)
    -- IC-1 : The boat len must be <= max_len
    -- IC-11 : cni is assigned by the country where the boat is registered
);



CREATE TABLE Jurisdictions(
    name VARCHAR(80),
    PRIMARY KEY (name)
    -- disjoint property
);

CREATE TABLE International(
    jurisdiction_name VARCHAR(80),
    PRIMARY KEY (jurisdiction_name),
    FOREIGN KEY (jurisdiction_name) REFERENCES Jurisdictions(name)
);

CREATE TABLE National(
    jurisdiction_name VARCHAR(80),
    enforced_by VARCHAR(3) NOT NULL,
    PRIMARY KEY (jurisdiction_name),
    FOREIGN KEY (jurisdiction_name) REFERENCES Jurisdictions(name),
    FOREIGN KEY (enforced_by) REFERENCES Country(iso)
);

CREATE TABLE Sailor(
    first_name VARCHAR(80) NOT NULL,
    surname VARCHAR(80) NOT NULL,
    email VARCHAR(254),
    primary key (email),
    CHECK (email LIKE '%@%.%') -- IC12
    -- disjointness check and mandatory check
);

CREATE TABLE Senior(
    email VARCHAR(254),
    PRIMARY KEY (email),
    FOREIGN KEY (email) REFERENCES Sailor(email)
);


CREATE TABLE Junior(
    email VARCHAR(254),
    PRIMARY KEY (email),
    FOREIGN KEY (email) REFERENCES Sailor(email)
);


CREATE TABLE Reservation(
    made_for_country VARCHAR(3) NOT NULL,
    made_for_boat_cni INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    responsible_email VARCHAR(254) NOT NULL,
    PRIMARY KEY (made_for_country, made_for_boat_cni, start_date, end_date),
    FOREIGN KEY (responsible_email) REFERENCES Senior(email),
    FOREIGN KEY (made_for_country, made_for_boat_cni) REFERENCES Boat(country_iso, cni),
    CHECK (start_date < end_date) -- IC10
    -- made_for table not required, represented by this table
    -- IC-9: The responsible senior sailor must be one of the sailors who made a joint registration
    -- IC-13 : trip dates must fall within reservation date, i.e. arrival_date >= start_date and trip_date <= end_date
    -- IC-20 : Reservations for the same boat must not have overlapping start_date and end_date intervals
);

CREATE TABLE reserves(
    email VARCHAR(254) NOT NULL,
    made_for_country VARCHAR(3) NOT NULL,
    made_for_boat_cni INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    PRIMARY KEY (email, made_for_country, made_for_boat_cni, start_date, end_date),
    FOREIGN KEY (email) REFERENCES Sailor(email),
    FOREIGN KEY (made_for_country, made_for_boat_cni, start_date, end_date) REFERENCES Reservation(made_for_country, made_for_boat_cni, start_date, end_date)
    -- IC-2 : A reservation must not consist of only Junior sailors
    -- IC-3 : Skipper must be one of the sailors from the reservation
    -- IC-9: The responsible senior sailor must be one of the sailors who made a joint registration
);

CREATE TABLE Location(
    name VARCHAR(70) NOT NULL,
    latitude NUMERIC(8,6) NOT NULL,
    longitude NUMERIC(9,6) NOT NULL,
    PRIMARY KEY (latitude, longitude),
    CHECK (latitude >= -90 AND latitude <= 90), --IC17
    CHECK (longitude >= -180 AND longitude <= 180) --IC18
    -- IC-4 : Any two locations must be at least one nautical mile apart

);


CREATE TABLE defines(
    country_iso VARCHAR(3) NOT NULL,
    latitude NUMERIC(8,6) NOT NULL,
    longitude NUMERIC(9,6) NOT NULL,
    PRIMARY KEY (latitude, longitude),
    FOREIGN KEY (country_iso) REFERENCES Country(iso),
    FOREIGN KEY (latitude, longitude) REFERENCES Location(latitude, longitude)
    -- IC-19 : Any country that registers boats must have at least one location defined
);


CREATE TABLE Trip(
    ins_ref VARCHAR(20),
    take_off_date DATE NOT NULL,
    arrival_date DATE NOT NULL,
    made_for_country_iso VARCHAR(3) NOT NULL,
    made_for_boat_cni INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    skipper_email VARCHAR(254) NOT NULL,
    start_loc_latitude NUMERIC(8,6) NOT NULL,
    start_loc_longitude NUMERIC(9,6) NOT NULL,
    end_loc_latitude NUMERIC(8,6) NOT NULL,
    end_loc_longitude NUMERIC(9,6) NOT NULL ,
    PRIMARY KEY (ins_ref),
    -- modelling for has association
    FOREIGN KEY (made_for_country_iso, made_for_boat_cni, start_date, end_date) REFERENCES
        Reservation(made_for_country, made_for_boat_cni, start_date, end_date),

    -- mandatory to one not needed, it has captured by this extension of Trip table

    -- modelling for skipper
    FOREIGN KEY (skipper_email) REFERENCES Sailor(email),
    -- mandatory to one not needed again

    -- modelling for location
    FOREIGN KEY (start_loc_latitude, start_loc_longitude) REFERENCES Location(latitude, longitude),
    FOREIGN KEY (end_loc_latitude, end_loc_longitude) REFERENCES Location(latitude, longitude),
    -- start location and end location can be same, no need to check

    CHECK (take_off_date <= arrival_date) -- IC15
    -- IC-5 : A skipper must have a certification for the jurisdiction and the boat class that has been reserved
    -- IC-6 : The certificate held by the skipper should have issue_date < take_off_date and expiry_date > arrival_date of the trip
    -- IC-13 : trip dates must fall within reservation date, i.e. arrival_date >= start_date and trip_date <= end_date
    -- IC-16 : Any 2 trips' active time windows should not overlap
);

CREATE TABLE lists(
    ins_ref VARCHAR(20),
    Jurisdiction_name VARCHAR(80),

    PRIMARY KEY (ins_ref, Jurisdiction_name),
    FOREIGN KEY (ins_ref) REFERENCES Trip(ins_ref),
    FOREIGN KEY (Jurisdiction_name) REFERENCES Jurisdictions(name)
    -- IC-7 : The skipper should have valid certifications for all jurisdictions listed in the trip
);

CREATE TABLE Certification(
    class_name VARCHAR(254) NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,

    PRIMARY KEY (class_name, issue_date, expiry_date),
    FOREIGN KEY (class_name) REFERENCES Class(class_name),

    CHECK ( issue_date < expiry_date ) -- IC14
    -- IC-6 : The certificate held by the skipper should have issue_date < take_off_date and expiry_date > arrival_date of the trip
);



CREATE TABLE acquires(
    class_name VARCHAR(80) NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    jurisdiction_name VARCHAR(80) NOT NULL,
    email VARCHAR(254) NOT NULL,
    PRIMARY KEY (email, issue_date, expiry_date, class_name, jurisdiction_name),
    FOREIGN KEY (jurisdiction_name) REFERENCES National(jurisdiction_name),
    FOREIGN KEY (class_name, issue_date, expiry_date) REFERENCES Certification(class_name, issue_date, expiry_date),
    FOREIGN KEY (email) REFERENCES Sailor(email)

    -- IC-5 : A skipper must have a certification for the jurisdiction and the boat class that has been reserved
);