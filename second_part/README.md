# Sailing Project - Part 5

This project implements a Database Application for the Sailing Project (Part 5) using Python. It includes both a **CGI Web Application** (prototype) and a **CLI Tool**.

## Prerequisites

- **Python 3.x**
- **PostgreSQL** database (remote or local).
- **psycopg2** library.

## Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Credentials**:
    - Open `login.py`.
    - Update the variables (`IST_ID`, `password`, `host`, etc.) with your specific PostgreSQL credentials.
    - **Note**: If connecting to `db.tecnico.ulisboa.pt`, ensure you are on the university network/VPN.

## Running the Web Application (CGI)

The web application allows you to manage Sailors, Reservations, Trips, and Authorizations via a browser interface.

1.  **Start a Local CGI Server**:
    The default python server configuration requires a specific folder structure (cgi-bin). To run the scripts from the current folder, use the provided `server.py` script:
    ```bash
    python server.py
    ```

2.  **Access the Application**:
    Open your web browser and go to:
    [http://localhost:8000/index.cgi](http://localhost:8000/index.cgi)

3.  **Features**:
    - **Manage Sailors**: List, Add (Junior/Senior), Remove.
    - **Manage Reservations**: Create, List, Delete.
    - **Manage Authorizations**: Link authorised sailors to a reservation.
    - **Manage Trips**: Register new trips (linked to reservations).

## Running the CLI Tool

A command-line interface provided earlier for executing specific SQL queries (Part 2 analysis).

1.  **Run**:
    ```bash
    python main.py
    ```
2.  **Menu Options**:
    - Query 1: Country with most boats.
    - Query 2: Sailors with multiple certificates.
    - Query 3: Sailors who sailed to every location in Portugal.
    - Query 4: Best Skipper statistics.

## Project Structure

- `*.cgi`: Python CGI scripts for the web interface.
- `login.py`: Configuration file for database credentials.
- `db.py`: Database connection helper.
- `main.py`: CLI application entry point.
- `requirements.txt`: Python dependencies.
