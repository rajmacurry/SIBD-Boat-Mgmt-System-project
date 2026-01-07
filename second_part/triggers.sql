SET search_path TO project_2;

-- =========================
-- DROP TRIGGERS
-- =========================

DROP TRIGGER IF EXISTS tg_check_mandatory_sailor_specialisation ON sailor;
DROP TRIGGER IF EXISTS tg_disjoint_junior_check ON junior;
DROP TRIGGER IF EXISTS tg_disjoint_senior_check ON senior;
DROP TRIGGER IF EXISTS tg_check_trip_overlap ON trip;

-- =========================
-- DROP FUNCTIONS
-- =========================

DROP FUNCTION IF EXISTS check_mandatory_sailor_specialisation();
DROP FUNCTION IF EXISTS disjoint_junior_check();
DROP FUNCTION IF EXISTS disjoint_senior_check();
DROP FUNCTION IF EXISTS check_trip_overlap();






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
       RETURNS TRIGGER AS
       $$
       BEGIN
       IF EXISTS (SELECT * FROM senior s WHERE s.email=NEW.email) THEN
          RAISE EXCEPTION 'Sailor cannot be both Junior and Senior';
       END IF;

       RETURN NEW;
       END;
       $$ LANGUAGE plpgsql;

CREATE  TRIGGER tg_disjoint_junior_check
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


CREATE  TRIGGER tg_disjoint_senior_check
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
    AND NEW.takeoff<arrival
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
    $$ LANGUAGE plpgsql;

CREATE TRIGGER tg_check_trip_overlap
BEFORE INSERT OR UPDATE ON trip
FOR EACH ROW
EXECUTE FUNCTION check_trip_overlap();
