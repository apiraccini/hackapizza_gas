from src.utils.questions import update_planet_keys


def test_update_planet_keys(tmp_path):
    questions = [
        {"planet": ["earth"], "planet_distance": 10},
        {"planet": ["mars"], "planet_distance": 40},
    ]
    distances_path = tmp_path / "distances.csv"
    distances_path.write_text("/,earth,mars\nearth,0,30\nmars,30,0\n")
    expected = [
        {"planet": ["earth"], "planet_distance": 10},
        {"planet": ["earth", "mars"], "planet_distance": 40},
    ]
    result = update_planet_keys(questions, distances_path)
    assert result == expected
