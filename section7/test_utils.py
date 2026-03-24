from main import calculate_grade


# Test Function

def test_calculate_grade_pass():
    assert calculate_grade(70) == "Pass"

def test_calculate_grade_fail():
    assert calculate_grade(30) == "Fail"