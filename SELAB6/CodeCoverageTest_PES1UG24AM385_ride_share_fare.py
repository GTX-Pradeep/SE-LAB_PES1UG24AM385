"""Lab 6 - Code (line) coverage tests for ride_share_fare.py
SRN: PES1UG24AM385
Goal: execute every line of the module at least once (>= 90% line coverage).
"""
import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ---------- extra_distance_fare ----------
def test_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_unknown_cab_type_raises():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 10, "city", False)


def test_negative_distance_raises():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_subscriber_city_short_extra():
    # mini: 5 + 3 (subscriber) = 8 included, extra = 2, city rate 12
    assert extra_distance_fare("mini", 10, "city", True) == 24


def test_outstation_long_extra():
    # suv: 12 included, extra = 28 (>20) -> rate 18 + 8 + 4 = 30
    assert extra_distance_fare("suv", 40, "outstation", False) == 28 * 30


# ---------- seats_and_bags_ok ----------
def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True


def test_wheelchair():
    assert seats_and_bags_ok(2, 0, True) is True


def test_too_many_passengers():
    assert seats_and_bags_ok(5, 0, False) is False


# ---------- pickup_status ----------
def test_scheduled_airport_on_time():
    # cutoff = 10 + 10 = 20
    assert pickup_status(20, True, True) == "on_time"


def test_unscheduled_delayed():
    # cutoff = 5, delayed if >= -10
    assert pickup_status(0, False, False) == "delayed"


def test_unscheduled_missed():
    assert pickup_status(-11, False, False) == "missed"
