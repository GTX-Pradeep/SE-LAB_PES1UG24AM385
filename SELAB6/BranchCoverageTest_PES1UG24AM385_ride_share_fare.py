"""Lab 6 - Branch coverage tests for ride_share_fare.py
SRN: PES1UG24AM385
Goal: every decision evaluates to both True and False (>= 90% branch coverage).
"""
import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ================= extra_distance_fare =================
# Branch 1: cab_type not in INCLUDED_KM  (True / False)
def test_unknown_cab_type_raises():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 10, "city", False)


# Branch 2: distance_km < 0  (True / False)
def test_negative_distance_raises():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_zero_distance_is_valid():
    assert extra_distance_fare("mini", 0, "city", False) == 0


# Branch 3: is_subscriber and cab_type != "suv"
def test_subscriber_non_suv_gets_bonus_km():
    # mini included 5 + 3 = 8 -> 8 km is free
    assert extra_distance_fare("mini", 8, "city", True) == 0


def test_subscriber_suv_no_bonus_km():
    # suv included stays 12 -> extra = 3, city rate 12
    assert extra_distance_fare("suv", 15, "city", True) == 36


def test_non_subscriber_no_bonus_km():
    # sedan included 8 -> extra = 2, city rate 12
    assert extra_distance_fare("sedan", 10, "city", False) == 24


# Branch 4: extra <= 0  (True / False, incl. boundary)
def test_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_exactly_included_distance():
    assert extra_distance_fare("sedan", 8, "city", False) == 0


def test_one_km_over_included():
    assert extra_distance_fare("sedan", 9, "city", False) == 12


# Branch 5: zone == "city"  (True / False)
def test_city_rate_short_trip():
    assert extra_distance_fare("mini", 15, "city", False) == 10 * 12


def test_non_city_rate_short_trip():
    assert extra_distance_fare("mini", 15, "suburb", False) == 10 * 18


# Branch 6: extra > 20  (True / False, boundary at 20)
def test_extra_exactly_20_no_surcharge():
    assert extra_distance_fare("mini", 25, "city", False) == 20 * 12


def test_extra_21_city_surcharge():
    # rate 12 + 8 = 20
    assert extra_distance_fare("mini", 26, "city", False) == 21 * 20


# Branch 7: zone == "outstation" inside long trip  (True / False)
def test_long_trip_outstation_extra_surcharge():
    # suv 12 included, extra 28 -> 18 + 8 + 4 = 30
    assert extra_distance_fare("suv", 40, "outstation", False) == 28 * 30


def test_long_trip_other_non_city_zone():
    # extra 28 -> 18 + 8 = 26 (no outstation bonus)
    assert extra_distance_fare("suv", 40, "suburb", False) == 28 * 26


# ================= seats_and_bags_ok =================
# Branch: needs_wheelchair (True) -> passengers <= 2
def test_wheelchair_ok():
    assert seats_and_bags_ok(2, 5, True) is True


def test_wheelchair_too_many_passengers():
    assert seats_and_bags_ok(3, 0, True) is False


# Branch: passengers > 4  (True / False)
def test_too_many_passengers():
    assert seats_and_bags_ok(5, 0, False) is False


def test_four_passengers_ok():
    assert seats_and_bags_ok(4, 2, False) is True


# Branch: bags <= 2
def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True


def test_too_many_bags():
    assert seats_and_bags_ok(2, 3, False) is False


# ================= pickup_status =================
# is_scheduled True/False x is_airport True/False, and all three outcomes
def test_scheduled_on_time():
    assert pickup_status(10, True, False) == "on_time"


def test_unscheduled_on_time():
    assert pickup_status(5, False, False) == "on_time"


def test_scheduled_airport_on_time():
    assert pickup_status(20, True, True) == "on_time"


def test_unscheduled_airport_delayed():
    # cutoff 15 -> delayed range [0, 15)
    assert pickup_status(14, False, True) == "delayed"


def test_delayed_boundary():
    # cutoff 5 -> cutoff - 15 = -10 is still delayed
    assert pickup_status(-10, False, False) == "delayed"


def test_missed():
    assert pickup_status(-11, False, False) == "missed"


def test_scheduled_airport_missed():
    # cutoff 20 -> missed below 5
    assert pickup_status(4, True, True) == "missed"
