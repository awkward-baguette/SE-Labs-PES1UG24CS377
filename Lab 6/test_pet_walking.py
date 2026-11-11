import pytest
from pet_walking_service import process_walking_routes, inspect_gps_collars

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