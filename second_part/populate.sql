------------------------------------------------------------
-- COUNTRY
------------------------------------------------------------
INSERT INTO country VALUES
('PRT','prt.png','Portugal'),
('ESP','esp.png','Spain'),
('FIN','fin.png','Fin.png'),
('DEU','deu.png','Germany'),
('FRA','fra.png','France'),
('ITA','ita.png','Italy');

------------------------------------------------------------
-- LOCATION (≥1 per country)
------------------------------------------------------------
INSERT INTO location VALUES
(37.019400,-7.932200,'Faro','Portugal'),
(38.722300,-9.139300,'Lisbon','Portugal'),
(41.149600,-8.610900,'Porto','Portugal'),

(36.527100,-6.288600,'Cadiz','Spain'),
(41.385100,2.173400,'Barcelona','Spain'),

(60.169900,24.938400,'Helsinki','Fin.png'),
(60.451800,22.266600,'Turku','Fin.png'),

(53.551100,9.993700,'Hamburg','Germany'),
(54.323300,10.122800,'Kiel','Germany'),

(43.296500,5.369800,'Marseille','France'),
(44.405600,8.946300,'Genoa','Italy');

------------------------------------------------------------
-- SAILOR

START TRANSACTION;
SET CONSTRAINTS ALL DEFERRED;


INSERT INTO sailor VALUES
('Raj','Maharjan','raj@mail.com'),
('Mohammad','Alsalman','mohammad@mail.com'),
('Ahmad','Ashraf','ahmad@mail.com'),
('Santeri','Kokkonen','santeri@mail.com'),
('Juan','Viteri','juan@mail.com'),
('Ana','Santos','ana@mail.com'),
('Joao','Silva','joao@mail.com'),
('Maria','Costa','maria@mail.com'),
('Laura','Bianchi','laura@mail.com'),
('Pierre','Dubois','pierre@mail.com');

INSERT INTO senior VALUES
('raj@mail.com'),
('ahmad@mail.com'),
('santeri@mail.com'),
('juan@mail.com'),
('ana@mail.com'),
('joao@mail.com');

INSERT INTO junior VALUES
('mohammad@mail.com'),
('maria@mail.com'),
('laura@mail.com'),
('pierre@mail.com');

COMMIT;

------------------------------------------------------------
-- BOAT CLASS
------------------------------------------------------------
INSERT INTO boat_class VALUES
('Class A',20),
('Class B',15),
('Class C',10);

------------------------------------------------------------
-- BOAT (Portugal has most boats)
------------------------------------------------------------
INSERT INTO boat VALUES
('Portugal',2018,'PT100','Atlantico',18,'Class A'),
('Portugal',2019,'PT101','Lusitano',14,'Class B'),
('Portugal',2020,'PT102','Tejo',10,'Class C'),
('Portugal',2017,'PT103','Douro',12,'Class B'),

('Spain',2016,'ES200','Iberico',15,'Class B'),
('Spain',2018,'ES201','Catalan',9,'Class C'),

('Fin.png',2020,'FI300','Aurora',14,'Class B'),
('Fin.png',2019,'FI301','Saimaa',10,'Class C'),

('Germany',2017,'DE400','Bremen',16,'Class A'),
('Germany',2015,'DE401','Oderwind',11,'Class B'),

('France',2021,'FR500','Azur',18,'Class A'),
('Italy',2022,'IT600','Liguria',14,'Class B');

------------------------------------------------------------
-- DATE INTERVAL
------------------------------------------------------------
INSERT INTO date_interval VALUES
('2025-01-01','2025-01-10'),
('2025-01-05','2025-01-20'),
('2025-02-01','2025-02-15'),
('2025-03-01','2025-03-20');

------------------------------------------------------------
-- SAILING CERTIFICATE
------------------------------------------------------------
INSERT INTO sailing_certificate VALUES
('2023-01-01','2026-01-01','raj@mail.com','Class A'),
('2024-01-01','2027-01-01','raj@mail.com','Class B'),

('2023-06-01','2026-06-01','ahmad@mail.com','Class A'),
('2024-02-01','2027-02-01','ahmad@mail.com','Class B'),

('2023-03-01','2026-03-01','santeri@mail.com','Class B'),
('2024-01-01','2027-01-01','juan@mail.com','Class C'),

('2023-05-01','2026-05-01','ana@mail.com','Class A'),
('2024-04-01','2027-04-01','ana@mail.com','Class B'),

('2024-06-01','2027-06-01','joao@mail.com','Class B');

------------------------------------------------------------
-- VALID_FOR (mandatory participation)
------------------------------------------------------------
INSERT INTO valid_for VALUES
('Portugal',20,'raj@mail.com','2023-01-01'),
('Spain',15,'raj@mail.com','2024-01-01'),

('Germany',20,'ahmad@mail.com','2023-06-01'),
('Fin.png',15,'ahmad@mail.com','2024-02-01'),

('Fin.png',15,'santeri@mail.com','2023-03-01'),
('Portugal',10,'juan@mail.com','2024-01-01'),

('Portugal',20,'ana@mail.com','2023-05-01'),
('France',15,'ana@mail.com','2024-04-01'),

('Portugal',15,'joao@mail.com','2024-06-01');

------------------------------------------------------------
-- RESERVATION (responsible is senior & authorized)
------------------------------------------------------------
INSERT INTO reservation VALUES
('2025-01-01','2025-01-10','Portugal','PT100','raj@mail.com'),
('2025-01-05','2025-01-20','Portugal','PT101','ana@mail.com'),
('2025-02-01','2025-02-15','Fin.png','FI300','santeri@mail.com'),
('2025-03-01','2025-03-20','Germany','DE400','ahmad@mail.com');

------------------------------------------------------------
-- AUTHORISED
------------------------------------------------------------
INSERT INTO authorised VALUES
('2025-01-01','2025-01-10','Portugal','PT100','raj@mail.com'),
('2025-01-01','2025-01-10','Portugal','PT100','juan@mail.com'),
('2025-01-01','2025-01-10','Portugal','PT100','ana@mail.com'),

('2025-01-05','2025-01-20','Portugal','PT101','ana@mail.com'),
('2025-01-05','2025-01-20','Portugal','PT101','joao@mail.com'),
('2025-01-05','2025-01-20','Portugal','PT101','maria@mail.com'),

('2025-02-01','2025-02-15','Fin.png','FI300','santeri@mail.com'),
('2025-02-01','2025-02-15','Fin.png','FI300','ahmad@mail.com'),

('2025-03-01','2025-03-20','Germany','DE400','ahmad@mail.com'),
('2025-03-01','2025-03-20','Germany','DE400','raj@mail.com');

------------------------------------------------------------
-- TRIP
------------------------------------------------------------
INSERT INTO trip VALUES
('2025-01-02','2025-01-04','INS001',
 37.019400,-7.932200,38.722300,-9.139300,
 'raj@mail.com','2025-01-01','2025-01-10','Portugal','PT100'),

('2025-01-06','2025-01-08','INS002',
 38.722300,-9.139300,41.149600,-8.610900,
 'juan@mail.com','2025-01-01','2025-01-10','Portugal','PT100'),

('2025-01-10','2025-01-14','INS003',
 37.019400,-7.932200,36.527100,-6.288600,
 'ana@mail.com','2025-01-05','2025-01-20','Portugal','PT101'),

('2025-01-15','2025-01-18','INS004',
 36.527100,-6.288600,41.385100,2.173400,
 'joao@mail.com','2025-01-05','2025-01-20','Portugal','PT101'),

('2025-02-03','2025-02-07','INS005',
 60.169900,24.938400,60.451800,22.266600,
 'santeri@mail.com','2025-02-01','2025-02-15','Fin.png','FI300'),

('2025-03-05','2025-03-12','INS006',
 53.551100,9.993700,54.323300,10.122800,
 'ahmad@mail.com','2025-03-01','2025-03-20','Germany','DE400');

INSERT INTO trip VALUES
(
 '2025-01-08','2025-01-09','INS007',
 38.722300,-9.139300,   -- Lisbon
 37.019400,-7.932200,   -- Faro
 'raj@mail.com',
 '2025-01-01','2025-01-10','Portugal','PT100'
);