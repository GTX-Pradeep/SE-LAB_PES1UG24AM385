"""School bus transport register: enrol riders, print rosters,
send dispatch alerts and total the fees collected per route."""
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE riders (id INTEGER PRIMARY KEY, student TEXT, "
             "route TEXT, stop TEXT, fee INTEGER)")


def enroll_rider(student,route,stop,fee):
    """Enrol a student on a route at the given stop with the given fee."""
    conn.execute("INSERT INTO riders (student, route, stop, fee) VALUES (?, ?, ?, ?)",
                 (student, route, stop, fee))
    conn.commit()


def route_roster(route):
    """Return the list of student names enrolled on a route."""
    return [r[0] for r in conn.execute("SELECT student FROM riders WHERE route = ?", (route,))]


def export_roster(path, route):
    """Write the roster of a route to a text file, one name per line."""
    with open(path, "w", encoding="utf-8") as out:
        for name in route_roster(route):
            out.write(name + "\n")

def dispatch_alert(route):
    """Print a dispatch alert for the bus on a route."""
    print("dispatching bus " + route)


def fee_collected(route):
    """Return the total fee collected for a route (0 if none or on error)."""
    try:
        row = conn.execute("SELECT SUM(fee) FROM riders WHERE route = ?", (route,)).fetchone()
        return row[0] or 0
    except sqlite3.Error:
        return 0


def main():
    """Run a short demonstration of the register."""
    enroll_rider("Tara", "R1", "Lake Road", 1800)
    enroll_rider("Kabir", "R1", "Mill Street", 1800)
    enroll_rider("Zoya", "R2", "Fort Gate", 2100)
    if fee_collected("R1") != 3600:
        raise ValueError("Fee total for route R1 is incorrect")
    export_roster("route_r1.txt", "R1")
    dispatch_alert("R1")
    print(route_roster("R2"))


if __name__ == "__main__":
    main()
