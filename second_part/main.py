from db import Database

def print_header(title):
    print("\n" + "=" * 40)
    print(f" {title}")
    print("=" * 40)

def query_country_most_boats(db):
    print("\n--- Query: Country with most boats ---")
    query = """
    SELECT country, COUNT(*)
    FROM boat
    GROUP BY country
    HAVING COUNT(*) >= ALL (
        SELECT COUNT(*)
        FROM boat
        GROUP BY country
    );
    """
    results = db.execute_query(query)
    if results:
        for row in results:
            print(f"Country: {row[0]}, Count: {row[1]}")
    else:
        print("No results found or error.")

def query_sailors_two_certificates(db):
    print("\n--- Query: Sailors with at least two certificates ---")
    query = """
    SELECT s.firstname, s.surname 
    FROM sailor s
    WHERE s.email IN (
        SELECT sailor
        FROM sailing_certificate
        GROUP BY sailor
        HAVING COUNT(*) >= 2
    );
    """
    results = db.execute_query(query)
    if results:
        for row in results:
            print(f"Sailor: {row[0]} {row[1]}")
    else:
        print("No results found.")

def query_sailors_every_location_portugal(db):
    print("\n--- Query: Sailors who sailed to every location in Portugal ---")
    # Using the division logic from triggers.sql
    query = """
    SELECT s.firstname, s.surname
    FROM sailor s
    WHERE NOT EXISTS (
        SELECT l.latitude, l.longitude
        FROM location l
        WHERE l.country_name = 'Portugal'
        EXCEPT
        SELECT t.to_latitude, t.to_longitude
        FROM trip t
        JOIN authorised a ON a.start_date = t.reservation_start_date
            AND a.end_date = t.reservation_end_date
            AND a.boat_country = t.boat_country
            AND a.cni = t.cni
        WHERE a.sailor = s.email
    );
    """
    results = db.execute_query(query)
    if results:
        for row in results:
            print(f"Sailor: {row[0]} {row[1]}")
    else:
        print("No results found.")

def query_best_skipper(db):
    print("\n--- Query: Skipper with max total sailing days per reservation ---")
    # Logic extracted from triggers.sql (at the end)
    query = """
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
            AND a.sailor       = t.skipper
        GROUP BY
            t.reservation_start_date, t.reservation_end_date, t.boat_country, t.cni,
            t.skipper
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
        s.email,
        s.firstname,
        s.surname,
        r.total_days
    FROM ranked r
    JOIN sailor s ON s.email = r.skipper
    WHERE r.total_days = r.max_days_in_res
    ORDER BY r.reservation_start_date, r.reservation_end_date, r.boat_country, r.cni;
    """
    results = db.execute_query(query)
    if results:
        # Print header
        print(f"{'Start Date':<12} {'End Date':<12} {'Country':<15} {'CNI':<10} {'Name':<20} {'Days':<5}")
        print("-" * 80)
        for row in results:
            # row: start, end, boat_country, cni, email, firstname, surname, total_days
            start, end, country, cni, email, fname, lname, days = row
            name = f"{fname} {lname}"
            print(f"{str(start):<12} {str(end):<12} {country:<15} {cni:<10} {name:<20} {days:<5}")
    else:
        print("No results found.")

def main():
    print_header("Sailing Project - Part 5 App")

    db = Database()
    if not db.connect():
        print("Exiting application due to connection failure.")
        return

    while True:
        print("\nSelect an operation:")
        print("1. Which country has more boats registered than any other?")
        print("2. List sailors with at least two certificates")
        print("3. Sailors who sailed to every location in Portugal")
        print("4. Skipper with longest sailing duration per reservation")
        print("0. Exit")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            query_country_most_boats(db)
        elif choice == '2':
            query_sailors_two_certificates(db)
        elif choice == '3':
            query_sailors_every_location_portugal(db)
        elif choice == '4':
            query_best_skipper(db)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

    db.close()

if __name__ == "__main__":
    main()
