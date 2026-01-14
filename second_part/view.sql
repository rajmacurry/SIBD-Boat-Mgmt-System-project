SET search_path TO project_2;

CREATE OR REPLACE VIEW trip_info AS
SELECT
    co.iso_code  AS country_iso_origin,
    co.name      AS country_name_origin,

    cd.iso_code  AS country_iso_dest,
    cd.name      AS country_name_dest,

    lo.name      AS loc_name_origin,
    ld.name      AS loc_name_dest,

    b.cni        AS cni_boat,
    cb.iso_code  AS country_iso_boat,
    cb.name      AS country_name_boat,

    t.takeoff    AS trip_start_date
FROM trip t
-- origin location
JOIN location lo
  ON lo.latitude  = t.from_latitude
 AND lo.longitude = t.from_longitude
-- destination location
JOIN location ld
  ON ld.latitude  = t.to_latitude
 AND ld.longitude = t.to_longitude

-- origin country
JOIN country co
  ON co.name = lo.country_name
-- destination country
JOIN country cd
  ON cd.name = ld.country_name

-- boat (country_name_boat, cni_boat is FK(Boat))
JOIN boat b
  ON b.country = t.boat_country
 AND b.cni     = t.cni
-- boat country iso/name
JOIN country cb
  ON cb.name = b.country;


select * from trip_info;