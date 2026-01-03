-- SET search_path TO project;

select boat_name from trip as t left outer join boat as b on t.made_for_boat_cni=b.cni;

(select boat_name from boat)
except
(select boat_name from trip as t left outer join boat as b on t.made_for_boat_cni=b.cni);



SELECT b.boat_name FROM Boat AS b
JOIN Country AS c ON b.country_iso = c.iso
JOIN Reservation AS r ON b.cni = r.made_for_boat_cni
JOIN Sailor AS s ON r.responsible_email = s.email
WHERE s.surname LIKE '%Santos' AND c.iso = 'PRT';

SELECT DISTINCT s.first_name, s.surname
FROM (Trip AS t JOIN Boat AS b ON b.cni = t.made_for_boat_cni JOIN
    Sailor AS s ON s.email = t.skipper_email) LEFT JOIN
    acquires AS a on a.email = s.email and a.class_name = b.class_name
WHERE a.email IS NULL;


