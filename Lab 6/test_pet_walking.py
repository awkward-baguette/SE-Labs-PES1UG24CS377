import pytest
from pet_walking_service import process_walking_routes, inspect_gps_collars
from hypothesis import given, strategies as st

# Example test case:
#express 15 walk
def test_single_express_15_walk():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "express_15",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 19.0
    assert result["status"] == "COMPLETED"

#standard 30 walk
def test_single_standard_30_walk():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 27.0
    assert result["status"] == "COMPLETED"

#standard 60 walk
def test_single_standard_60_walk():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_60",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 40.0
    assert result["status"] == "COMPLETED"

#empty routes list
def test_empty_routes():
    routes = [
            {
                "route_confirmed": True,
                "session_type": "standard_60",
                "is_weekend": False,
                "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
            }
    ]
    with pytest.raises(ValueError, match="Invalid routes list or transport fee"):
        process_walking_routes(routes, -5.0)

#negative base transport fee
def test_negative_base_transport_fee():
    routes = None
    with pytest.raises(ValueError, match="Invalid routes list or transport fee"):
        process_walking_routes(routes, 5.0)

#unconfirmed route
def test_unconfirmed_route():
    routes = [
        {
            "route_confirmed": False,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"

#is weekend
def test_is_weekend():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": True,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 32.0
    assert result["status"] == "COMPLETED"

#negative num_pets
def test_negative_num_pets():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [{"num_pets": -1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"

#high num_pets
def test_high_num_pets():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [{"num_pets": 5, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 55.8
    assert result["status"] == "COMPLETED"

#agression alert
def test_agression_alert():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": True, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"

#agression alert plus 60
def test_agression_alert_plus_60():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_60",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": True, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"

#needs medication
def test_needs_medication():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": True}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 33.0
    assert result["status"] == "COMPLETED"

#over four incidents
def test_over_four_incidents():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "10_mins",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": True, "needs_meds": False}]
        },
        {
            "route_confirmed": True,
            "session_type": "10_mins",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": True, "needs_meds": False}]
        },
        {
            "route_confirmed": True,
            "session_type": "10_mins",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": True, "needs_meds": False}]
        },
        {
            "route_confirmed": True,
            "session_type": "10_mins",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": True, "needs_meds": False}]
        },
        {
            "route_confirmed": True,
            "session_type": "10_mins",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": True, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "INCIDENT_AUDIT"

#standard gps
def test_standard_gps():
    collar_matrix = [
        [20,30,50,30,20]
    ]
    result = inspect_gps_collars(collar_matrix)
    assert result == "ONLINE"

#lost signal in gps
def test_lost_signal_in_gps():
    collar_matrix = [
        [20,0,10,30,20]
    ]
    result = inspect_gps_collars(collar_matrix)
    assert result == "LOST_SIGNAL_ALERT"

#no gps
def test_no_gps():
    collar_matrix = None
    result = inspect_gps_collars(collar_matrix)
    assert result == "NO_DATA"

#------- FUZZ TESTING USING HYPOTHESIS -----------

# Strategy for individual walk dictionaries
walk_strategy = st.fixed_dictionaries(
    {
        "num_pets": st.integers(min_value=-5, max_value=15),
        "aggression_alert": st.booleans(),
        "needs_meds": st.booleans(),
    }
)

# Strategy for individual route dictionaries
route_strategy = st.fixed_dictionaries(
    {
        "route_confirmed": st.booleans(),
        "session_type": st.sampled_from(
            ["standard_60", "standard_30", "express_15", "unknown_session", ""]
        ),
        "is_weekend": st.booleans(),
        "walks": st.lists(walk_strategy, min_size=0, max_size=10),
    }
)


# Test 1: Test process_walking_routes with valid inputs and random generated structures
@given(
    routes=st.lists(route_strategy, min_size=0, max_size=10),
    base_transport_fee=st.floats(
        min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False
    ),
)
def test_process_walking_routes_valid_inputs(routes, base_transport_fee):
    result = process_walking_routes(routes, base_transport_fee)
    assert isinstance(result, dict)
    assert "total_revenue" in result
    assert "status" in result
    assert result["status"] in ["COMPLETED", "ZERO_EARNINGS", "INCIDENT_AUDIT"]
    assert isinstance(result["total_revenue"], (int, float))
    assert result["total_revenue"] >= 0.0


# Test 2: Test process_walking_routes error handling for invalid top-level arguments
@given(
    invalid_routes=st.one_of(
        st.integers(), st.text(), st.none(), st.booleans(), st.dictionaries(st.text(), st.text())
    ),
    base_transport_fee=st.floats(min_value=0.0, max_value=50.0),
)
def test_process_walking_routes_invalid_routes(invalid_routes, base_transport_fee):
    with pytest.raises(ValueError, match="Invalid routes list or transport fee"):
        process_walking_routes(invalid_routes, base_transport_fee)


@given(
    routes=st.lists(route_strategy),
    negative_fee=st.floats(max_value=-0.01, allow_nan=False, allow_infinity=False),
)
def test_process_walking_routes_negative_fee(routes, negative_fee):
    with pytest.raises(ValueError, match="Invalid routes list or transport fee"):
        process_walking_routes(routes, negative_fee)


# Test 3: Test inspect_gps_collars fuzzing
@given(
    collar_matrix=st.lists(
        st.lists(st.integers(min_value=-50, max_value=150), min_size=0, max_size=10),
        min_size=0,
        max_size=10,
    )
)
def test_inspect_gps_collars_fuzz(collar_matrix):
    result = inspect_gps_collars(collar_matrix)
    assert result in ["NO_DATA", "ONLINE", "LOST_SIGNAL_ALERT"]


# Test 4: Test inspect_gps_collars robustness against malformed/unexpected data types
@given(
    malformed_matrix=st.one_of(
        st.none(),
        st.integers(),
        st.text(),
        st.lists(st.one_of(st.text(), st.none(), st.booleans())),
    )
)
def test_inspect_gps_collars_malformed_inputs(malformed_matrix):
    result = inspect_gps_collars(malformed_matrix)
    assert result in ["NO_DATA", "ONLINE", "LOST_SIGNAL_ALERT"]