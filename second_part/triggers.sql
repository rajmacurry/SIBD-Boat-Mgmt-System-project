--IC1
CREATE OR REPLACE FUNCTION check_mandatory_sailor_specialisation()
       RETURNS TRIGGER AS
       $$
       BEGIN
       IF NEW.email NOT in (SELECT email from junior UNION Select email from senior) THEN
          RAISE EXCEPTION 'Sailor must be either a senior or a junior';
       END IF;

       RETURN NEW;
       END;
       $$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER tg_check_mandatory_sailor_specialisation
AFTER INSERT ON sailor DEFERRABLE
FOR EACH ROW EXECUTE PROCEDURE check_mandatory_sailor_specialisation();

-- Trigger on Junior table, checks if sailor is already senior
CREATE OR REPLACE FUNCTION disjoint_junior_check()
       RETURN TRIGGER AS
       $$
       BEGIN
       IF EXISTS (SELECT * FROM senior s WHERE s.email=NEW.email) THEN
          RAISE EXCEPTION 'Sailor cannot be both Junior and Senior';
       END IF;

       RETURN NEW;
       END;
       $$ LANGUAGE plpgsql;

CREATE TRIGGER tg_disjoint_junior_check
BEFORE INSERT OR UPDATE OF email on junior
FOR EACH ROW EXECUTE PROCEDURE disjoint_junior_check();

CREATE OR REPLACE FUNCTION disjoint_senior_check()
    RETURNS TRIGGER AS
    $$
    BEGIN
    IF EXISTS (SELECT * FROM junior j WHERE j.email=NEW.email) THEN
        RAISE EXCEPTION 'Sailor cannot be both Junior and Senior';
    END IF;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;


CREATE TRIGGER tg_disjoint_senior_check
BEFORE INSERT OR UPDATE OF email ON senior
FOR EACH ROW EXECUTE PROCEDURE disjoint_senior_check();

--IC2



CREATE OR REPLACE FUNCTION check_trip_overlap()
RETURNS TRIGGER AS
$$
    BEGIN
    IF EXISTS (
    SELECT * FROM TRIP WHERE reservation_start_date=New.reservation_start_date AND
    reservation_end_date=NEW.reservation_end_date AND boat_country=NEW.boat_country AND cni=NEW.CNI
    -- check if the new trip takes off before an ongoing trip arrives
    AND NEW.take_off<arrival
    --check if the new trip arrives after the an existing trip was meant to take off
    AND NEW.arrival>takeoff
    --If we are updating a trip, we dont want the system to think that the trip is overlapping with itself.
    AND NOT (takeoff=OLD.takeoff AND reservation_start_date=OLD.reservation_start_date
    AND reservation_end_date=OLD.reservation_end_date
    AND boat_country= OLD.boat_country and cni=OLD.cni))
    THEN
    RAISE EXCEPTION 'Trip dates overlap with an existing trip for this reservation'; --return which trips overlap
    END IF;

    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql

CREATE TRIGGER tg_check_trip_overlap
BEFORE INSERT OR UPDATE ON trip
FOR EACH ROW
EXECUTE FUNCTION check_trip_overlap();


-------------------------------- SQL----------------------------------
--Which country has more boats registered than any other?
SELECT country, COUNT(*)
FROM boat
GROUP BY country
HAVING COUNT(*)>= ALL (SELECT COUNT(*)
                       FROM boat
                       GROUP BY country
);

--List all the sailors that have at least two certificates.
SElECT s.firstname, s.surname FROM sailor s
JOIN (SELECT sailor
FROM sailing_certificate
GROUP BY sailor
HAVING COUNT(*)>=2) sc ON sc.sailor=s.email;

select s.firstname, s.surname from sailor s
where s.email in (select sailor
                  from sailing_certificate sc
                  group by sailor
                  having count(*)>=2);


--Who are the sailors that have sailed to every location in 'Portugal'?
-- this has to be division,

-- SELECT DISTINCT First_name,Sur_name From Sailor
-- WHERE NOT EXISTS( Sailed locations in

--we need to first find the table that relates sailors with locations and trips this is the mega join and then we need to cross join in with the
SELECT s.first_name, s.surname FROM sailor s WHERE NOT EXISTS
    (SELECT l.name FROM location l JOIN trip t
        -- joined it on the to_latitude and to_longitude because the question asked sailed TO every location
    ON l.latitude=t.to_latitude AND l.longitude=t.to_longitude
    JOIN reservation r ON t.reservation_start_date=r.start_date AND t.reservation_end_date=r.end_date AND t.boat_country=r.country and t.cni=r.cni
    JOIN authorised a ON a.start_date=r.start_date AND a.end_date=r.end_date AND a.boat_country=r.country AND a.cni=r.cni
    JOIN s ON a.sailor=s.email where l.country_name='Portugal' )
EXCEPT (SELECT l.name from location where country_name='Portugal');



SET search_path TO project_2;

SELECT DISTINCT s.firstname, s.surname
FROM sailor s
WHERE NOT EXISTS (
    -- All Portugal locations (set B)
    SELECT l.latitude, l.longitude
    FROM location l
    WHERE l.country_name = 'Portugal'

    EXCEPT

    -- Locations in Portugal that THIS sailor has sailed TO (set B for this A)
    SELECT t.to_latitude, t.to_longitude
    FROM trip t
             JOIN authorised a
                  ON a.start_date   = t.reservation_start_date
                      AND a.end_date     = t.reservation_end_date
                      AND a.boat_country = t.boat_country
                      AND a.cni          = t.cni
    WHERE a.sailor = s.email
);


SELECT country, COUNT(*)
FROM boat
GROUP BY country
HAVING COUNT(*)>= ALL (SELECT COUNT(*)
                       FROM boat
                       GROUP BY country
);

select s.firstname, s.surname
from sailor s
where s.email in (
    select t.skipper
    from trip t
    group by skipper
    having count(*) >= all (
        select count(*)
        from trip
        group by skipper
        )
    );



SELECT * FROM trip

SELECT skipper,
       reservation_start_date,
       reservation_end_date,
       boat_country,
       cni,
       SUM(arrival - takeoff) AS total_days
FROM trip
GROUP BY skipper,
         reservation_start_date,
         reservation_end_date,
         boat_country,
         cni
HAVING SUM(arrival - takeoff) >= ALL (
    SELECT SUM(arrival - takeoff)
    FROM trip
    GROUP BY skipper,
             reservation_start_date,
             reservation_end_date,
             boat_country,
             cni
);








SELECT
    s.firstname,
    s.surname,
    SUM(t.arrival - t.takeoff) AS total_days
FROM trip t
         JOIN sailor s ON s.email = t.skipper
GROUP BY
    s.firstname,
    s.surname,
    t.reservation_start_date,
    t.reservation_end_date,
    t.boat_country,
    t.cni
HAVING SUM(t.arrival - t.takeoff) >= ALL (
    SELECT SUM(arrival - takeoff)
    FROM trip
    GROUP BY
        skipper,
        reservation_start_date,
        reservation_end_date,
        boat_country,
        cni
);



SELECT t.skipper,
       t.reservation_start_date,
       t.reservation_end_date,
       t.boat_country,
       t.cni,
       SUM(t.arrival - t.takeoff) AS total_days
FROM trip t
         JOIN authorised a
              ON a.start_date   = t.reservation_start_date
                  AND a.end_date     = t.reservation_end_date
                  AND a.boat_country = t.boat_country
                  AND a.cni          = t.cni
                  AND a.sailor       = t.skipper              -- <- skipper must be authorised
GROUP BY t.skipper,
         t.reservation_start_date,
         t.reservation_end_date,
         t.boat_country,
         t.cni
HAVING SUM(t.arrival - t.takeoff) >= ALL (
    SELECT SUM(t2.arrival - t2.takeoff)
    FROM trip t2
             JOIN authorised a2
                  ON a2.start_date   = t2.reservation_start_date
                      AND a2.end_date     = t2.reservation_end_date
                      AND a2.boat_country = t2.boat_country
                      AND a2.cni          = t2.cni
                      AND a2.sailor       = t2.skipper
    GROUP BY t2.skipper,
             t2.reservation_start_date,
             t2.reservation_end_date,
             t2.boat_country,
             t2.cni
);


select t.country_name,
       t.cni,
       t.start_date,
       t.end_date,
       t.sailo_id / email,
       SUM(t.arrival - t.take_off) AS total_duration
from trip t
group by t.country_name, t.cni, t.start_date, t.end_date, t.sailo_id / email
having SUM(t.arrival - t.take_off) = (select max(total_dur)
                                      from (select t2.sailor_id, SUM(t.arrival - t.take_off) as total_dur
                                            from trip t2
                                            where t2.country_name = t.country_name, t2.cni = t.cni, t2.start_date = t.start_date, t2.end_date = t.end_date));

WITH per_sailor_res AS (
    SELECT
        t.reservation_start_date,
        t.reservation_end_date,
        t.boat_country,
        t.cni,
        t.skipper,
        SUM(t.arrival - t.takeoff) AS total_days
    FROM trip t
             JOIN authorised a
                  ON a.start_date   = t.reservation_start_date
                      AND a.end_date     = t.reservation_end_date
                      AND a.boat_country = t.boat_country
                      AND a.cni          = t.cni
                      AND a.sailor       = t.skipper          -- skipper must be authorised
    GROUP BY
        t.reservation_start_date, t.reservation_end_date, t.boat_country, t.cni,
        t.skipper
),
     auth_list AS (
         SELECT
             a.start_date,
             a.end_date,
             a.boat_country,
             a.cni,
             ARRAY_AGG(a.sailor ORDER BY a.sailor) AS authorised_sailors
         FROM authorised a
         GROUP BY a.start_date, a.end_date, a.boat_country, a.cni
     ),
     ranked AS (
         SELECT
             p.*,
             MAX(total_days) OVER (
                 PARTITION BY reservation_start_date, reservation_end_date, boat_country, cni
                 ) AS max_days_in_res
         FROM per_sailor_res p
     )
SELECT
    r.reservation_start_date,
    r.reservation_end_date,
    r.boat_country,
    r.cni,
    s.email        AS sailor_email,
    s.firstname,
    s.surname,
    r.total_days,
    al.authorised_sailors
FROM ranked r
         JOIN sailor s
              ON s.email = r.skipper
         JOIN auth_list al
              ON al.start_date   = r.reservation_start_date
                  AND al.end_date     = r.reservation_end_date
                  AND al.boat_country = r.boat_country
                  AND al.cni          = r.cni
WHERE r.total_days = r.max_days_in_res      -- keep the best skipper(s) per reservation (ties included)
ORDER BY r.reservation_start_date, r.reservation_end_date, r.boat_country, r.cni, sailor_email;
