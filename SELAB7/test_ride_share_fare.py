from hypothesis import given, settings, strategies as st
from ride_share_fare import parse_trip, fare_average, payable_fare

# Mix totally random text with "almost valid" inputs so Hypothesis
# reaches the deeper parsing logic, not just the split() step.
num = st.one_of(
    st.integers(-10**6, 10**6).map(str),
    st.floats(allow_nan=True, allow_infinity=True).map(str),
    st.sampled_from(["", " ", "nan", "inf", "-inf", "abc", "1e400", "0"]),
)

trip_inputs = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.builds(lambda a, b: f"{a}:{b}", st.text(max_size=10), num),
    st.builds(lambda a, b, c: f"{a}:{b}:{c}", st.text(max_size=5), num, num),
)

fare_inputs = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.lists(num, max_size=6).map(",".join),
)

payable_inputs = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.builds(lambda a, b: f"{a}|{b}", num, num),
    st.builds(lambda a, b, c: f"{a}|{b}|{c}", num, num, num),
)


@settings(max_examples=500)
@given(trip_inputs)
def test_parse_trip_no_crash(s):
    try:
        result = parse_trip(s)
    except Exception as e:
        assert False, f"parse_trip crashed on {s!r} with: {type(e).__name__}: {e}"
    # Property: returns None for invalid input, or (cab, finite non-negative km)
    if result is not None:
        cab, km = result
        assert isinstance(cab, str) and cab != ""
        assert km >= 0 and km != float("inf") and km == km


@settings(max_examples=500)
@given(fare_inputs)
def test_fare_average_no_crash(s):
    try:
        result = fare_average(s)
    except Exception as e:
        assert False, f"fare_average crashed on {s!r} with: {type(e).__name__}: {e}"
    if result is not None:
        assert result >= 0


@settings(max_examples=500)
@given(payable_inputs)
def test_payable_fare_no_crash(s):
    try:
        result = payable_fare(s)
    except Exception as e:
        assert False, f"payable_fare crashed on {s!r} with: {type(e).__name__}: {e}"
    if result is not None:
        assert result >= 0 and result == result and result != float("inf")
