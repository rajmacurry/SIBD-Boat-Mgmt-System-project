SET search_path TO project_2;
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

select s.firstname, s.surname from sailor s
where s.email in (select sailor
                  from sailing_certificate sc
                  group by sailor
                  having count(*)>=2);


--Who are the sailors that have sailed to every location in 'Portugal'?
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



-- List the sailors with the most skipped trips

select s.firstname, s.surname
from sailor s
where s.email in (select t.skipper
                  from trip t
                  group by skipper
                  having count(*) >= all (select count(*)
                                          from trip
                                          group by skipper));



-- list the sailors with the longest duration of trips(sum of trip durations) for the same single reservations; display also the sum of trips duration


select s.*, a.start_date, a.end_date, a.boat_country, a.cni, total_days
from sailor s inner join authorised a on s.email = a.sailor
inner join (SELECT
    t.reservation_start_date AS start_date,
    t.reservation_end_date   AS end_date,
    t.boat_country           AS boat_country,
    t.cni,
    SUM(t.arrival - t.takeoff) AS total_days
FROM trip t
GROUP BY
    t.reservation_start_date,
    t.reservation_end_date,
    t.boat_country,
    t.cni
HAVING SUM(t.arrival - t.takeoff) >= ALL (
    SELECT SUM(t2.arrival - t2.takeoff)
    FROM trip t2
    GROUP BY
        t2.reservation_start_date,
        t2.reservation_end_date,
        t2.boat_country,
        t2.cni
)) m on m.start_date = a.start_date and m.end_date = a.end_date
and m.boat_country = a.boat_country and m.cni = a.cni;


