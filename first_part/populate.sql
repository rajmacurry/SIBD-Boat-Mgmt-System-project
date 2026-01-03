-- SET search_path TO project;

------------------------------------------------------------
-- Countries
------------------------------------------------------------
INSERT INTO Country (iso, flag, name)
VALUES
    ('PRT', 'prt_flag.png', 'Portugal'),
    ('ESP', 'esp_flag.png', 'Spain'),
    ('FIN', 'fin_flag.png', 'Finland'),
    ('DEU', 'deu_flag.png', 'Germany');

------------------------------------------------------------
-- Classes
------------------------------------------------------------
INSERT INTO Class (class_name, max_len)
VALUES
    ('Class 1', 15),
    ('Class 2', 10);

------------------------------------------------------------
-- Boats
------------------------------------------------------------
INSERT INTO Boat (country_iso, boat_name, len, cni, year, class_name, image)
VALUES
    -- Portugal
    ('PRT', 'Atlantico', 12, 1001, 2018, 'Class 1', 'image1.png'),
    ('PRT', 'Lusitano', 9, 1002, 2016, 'Class 2', 'image2.png'),

    -- Finland
    ('FIN', 'Aurora', 14, 2001, 2020, 'Class 2', 'image3.png'),
    ('FIN', 'Saimaa', 8, 2002, 2015, 'Class 1', 'image4.png'),

    -- Germany
    ('DEU', 'Bremen Star', 11, 3001, 2019, 'Class 1', 'image5.png'),
    ('DEU', 'Oderwind', 7, 3002, 2012, 'Class 1', 'image6.png');

------------------------------------------------------------
-- Jurisdictions (ONLY National jurisdictions allowed)
------------------------------------------------------------
INSERT INTO Jurisdictions (name)
VALUES
    ('Portuguese EEZ'),
    ('Finnish Waters'),
    ('German Waters');

INSERT INTO National (jurisdiction_name, enforced_by)
VALUES
    ('Portuguese EEZ', 'PRT'),
    ('Finnish Waters', 'FIN'),
    ('German Waters', 'DEU');

------------------------------------------------------------
-- Sailors
------------------------------------------------------------
INSERT INTO Sailor (first_name, surname, email) VALUES
    ('Ana', 'Santos', 'ana.santos@mail.com'),
    ('Joao', 'Silva', 'joao.silva@mail.com'),
    ('Maria', 'Costa', 'maria.costa@mail.com'),
    ('Ahmad', 'Ashraf', 'ahmad.ashraf@mail.com'),
    ('Raj', 'Maharjan', 'raj.maharjan@mail.com'),
    ('Mohammad', 'Alsalman', 'mohammad.alsalman@mail.com'),
    ('Santeri', 'Kokonen', 'santeri.kokonen@mail.com');

-- Seniors (allowed to be responsible)
INSERT INTO Senior (email) VALUES
    ('ana.santos@mail.com'),
    ('joao.silva@mail.com'),
    ('ahmad.ashraf@mail.com'),
    ('santeri.kokonen@mail.com');

-- Juniors
INSERT INTO Junior (email) VALUES
    ('maria.costa@mail.com'),
    ('raj.maharjan@mail.com'),
    ('mohammad.alsalman@mail.com');

------------------------------------------------------------
-- Reservations
------------------------------------------------------------
-- Portugal reservation
INSERT INTO Reservation (made_for_country, made_for_boat_cni, start_date, end_date, responsible_email)
VALUES
    ('PRT', 1001, '2025-01-10', '2025-01-15', 'ana.santos@mail.com');

INSERT INTO reserves VALUES
    ('ana.santos@mail.com','PRT',1001,'2025-01-10','2025-01-15'),
    ('joao.silva@mail.com','PRT',1001,'2025-01-10','2025-01-15'),
    ('maria.costa@mail.com','PRT',1001,'2025-01-10','2025-01-15');

-- Finland reservation
INSERT INTO Reservation VALUES
    ('FIN', 2001, '2025-02-05', '2025-02-08', 'santeri.kokonen@mail.com');

INSERT INTO reserves VALUES
    ('santeri.kokonen@mail.com','FIN',2001,'2025-02-05','2025-02-08'),
    ('ahmad.ashraf@mail.com','FIN',2001,'2025-02-05','2025-02-08'),
    ('raj.maharjan@mail.com','FIN',2001,'2025-02-05','2025-02-08');

-- Germany reservation
INSERT INTO Reservation VALUES
    ('DEU', 3001, '2025-03-01', '2025-03-04', 'ahmad.ashraf@mail.com');

INSERT INTO reserves VALUES
    ('ahmad.ashraf@mail.com','DEU',3001,'2025-03-01','2025-03-04'),
    ('mohammad.alsalman@mail.com','DEU',3001,'2025-03-01','2025-03-04');

------------------------------------------------------------
-- Locations
------------------------------------------------------------
INSERT INTO Location (name, latitude, longitude)
VALUES
    ('Faro', 37.019400, -7.932200),
    ('Cadiz', 36.527100, -6.288600),
    ('Helsinki', 60.169900, 24.938400),
    ('Turku', 60.451800, 22.266600),
    ('Hamburg', 53.551100, 9.993700),
    ('Kiel', 54.323300, 10.122800);

INSERT INTO defines VALUES
    ('PRT', 37.019400, -7.932200),
    ('ESP', 36.527100, -6.288600),
    ('FIN', 60.169900, 24.938400),
    ('DEU', 53.551100, 9.993700);

------------------------------------------------------------
-- Trips
------------------------------------------------------------
-- Trip in Portugal
INSERT INTO Trip VALUES
(
    'INS-001', '2025-01-12', '2025-01-13',
    'PRT', 1001, '2025-01-10', '2025-01-15',
    'joao.silva@mail.com',
    37.019400, -7.932200,
    36.527100, -6.288600
);

-- Trip in Finland
INSERT INTO Trip VALUES
(
    'INS-002', '2025-02-06', '2025-02-07',
    'FIN', 2001, '2025-02-05', '2025-02-08',
    'santeri.kokonen@mail.com',
    60.169900, 24.938400,
    60.451800, 22.266600
);

-- Trip in Germany
INSERT INTO Trip VALUES
(
    'INS-003', '2025-03-02', '2025-03-03',
    'DEU', 3001, '2025-03-01', '2025-03-04',
    'ahmad.ashraf@mail.com',
    53.551100, 9.993700,
    54.323300, 10.122800
);

------------------------------------------------------------
-- Trip – Jurisdiction associations
------------------------------------------------------------
INSERT INTO lists (ins_ref, jurisdiction_name) VALUES
    ('INS-001', 'Portuguese EEZ'),
    ('INS-001', 'Finnish Waters'),

    ('INS-002', 'German Waters'),
    ('INS-002', 'Portuguese EEZ'),

    ('INS-003', 'Finnish Waters'),
    ('INS-003', 'German Waters');

------------------------------------------------------------
-- Certifications & Acquires
------------------------------------------------------------
INSERT INTO Certification VALUES
    ('Class 1', '2024-01-01', '2027-01-01'),
    ('Class 1', '2023-06-01', '2026-06-01'),
    ('Class 1', '2024-02-01', '2027-02-01'),
    ('Class 1', '2024-03-01', '2027-03-01');

INSERT INTO acquires VALUES
    ('Class 1','2024-01-01','2027-01-01','Portuguese EEZ','ana.santos@mail.com'),
    ('Class 1','2023-06-01','2026-06-01','Portuguese EEZ','joao.silva@mail.com'),
    ('Class 1','2024-02-01','2027-02-01','German Waters','ahmad.ashraf@mail.com'),
    ('Class 1','2024-03-01','2027-03-01','Finnish Waters','santeri.kokonen@mail.com');