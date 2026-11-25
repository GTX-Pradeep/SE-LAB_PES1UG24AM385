import math

GST_RATE = 1.18


def _to_number(value, as_int=False):
    """Convert a string to a finite, non-negative number. Return None if invalid."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    if value == "":
        return None
    try:
        number = int(value) if as_int else float(value)
    except (ValueError, OverflowError):
        return None
    if isinstance(number, float) and not math.isfinite(number):
        return None          # rejects nan, inf, -inf, 1e400
    if number < 0:
        return None          # negative distance / fare / promo makes no sense
    return number


def parse_trip(text):
    """'sedan:12' -> ('Sedan', 12.0). Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    cab = parts[0].strip()
    km = _to_number(parts[1])
    if cab == "" or km is None:
        return None
    return cab.title(), km


def fare_average(fares_csv):
    """'120,95,210' -> 141. Returns None for invalid input."""
    if not isinstance(fares_csv, str) or fares_csv.strip() == "":
        return None
    values = []
    for item in fares_csv.split(','):
        number = _to_number(item, as_int=True)
        if number is None:
            return None
        values.append(number)
    if not values:          # guards against ZeroDivisionError
        return None
    return sum(values) // len(values)


def payable_fare(text):
    """'250|30' -> 265.0 (fare + 18% GST - promo, never below 0). None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    fare = _to_number(parts[0])
    promo = _to_number(parts[1])
    if fare is None or promo is None:
        return None
    total = fare * GST_RATE - promo
    if not math.isfinite(total):
        return None          # overflow for extremely large fares
    return max(total, 0)


def _show(label, result, error_msg):
    if result is None:
        print(f"Invalid input: {error_msg}")
    else:
        print(label, result)


def main():
    try:
        print("==== Running parse_trip ====")
        user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
        _show("Cab and Distance:", parse_trip(user_input),
              "use the format cab:distance with a non-negative number")

        print("\n==== Running fare_average ====")
        user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
        _show("Average Fare:", fare_average(user_input),
              "enter non-negative whole numbers separated by commas")

        print("\n==== Running payable_fare ====")
        user_input = input("Enter fare|promo (e.g. 250|30): ")
        _show("Payable Fare:", payable_fare(user_input),
              "use the format fare|promo with non-negative numbers")
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Exiting.")


if __name__ == "__main__":
    main()
