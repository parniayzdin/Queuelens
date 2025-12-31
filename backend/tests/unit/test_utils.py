from utils import clamp, is_valid_lat_lng, normalize_query, iso_now

def test_clamp_middle():
    assert clamp(5, 0, 10) == 5

def test_clamp_low():
    assert clamp(-1, 0, 10) == 0

def test_clamp_high():
    assert clamp(999, 0, 10) == 10

def test_valid_lat_lng_true():
    assert is_valid_lat_lng(43.65, -79.38) is True

def test_valid_lat_lng_lat_low_false():
    assert is_valid_lat_lng(-91, 0) is False

def test_valid_lat_lng_lat_high_false():
    assert is_valid_lat_lng(91, 0) is False

def test_valid_lat_lng_lng_low_false():
    assert is_valid_lat_lng(0, -181) is False

def test_valid_lat_lng_lng_high_false():
    assert is_valid_lat_lng(0, 181) is False

def test_normalize_query_collapses_spaces():
    assert normalize_query("  hello   world  ") == "hello world"

def test_normalize_query_empty():
    assert normalize_query("") == ""

def test_iso_now_is_string():
    s = iso_now()
    assert isinstance(s, str)
    assert "T" in s
