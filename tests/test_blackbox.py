# Black-box tests for the registration system.
# Expected results come from REQUIREMENTS.md (not from registration.py).
# If two techniques (ECP/BVA/DT) needed exactly the same input we wrote
# the test only once and wrote both ids in the comment.

import pytest
from registration import Student, Course
from registration import check_credit_limit, prerequisites_satisfied
from registration import registration_decision, register_course, withdraw_course


# ---------- ECP ----------

def test_ecp01_normal_student():
    # same input as ecp04, ecp09, bva15, dt06
    s = Student("S001")
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "REGISTERED"


def test_ecp02_positive_dues():
    s = Student("S001", outstanding_dues=500)
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "DUES_BLOCK"


def test_ecp03_negative_dues():
    # same as bva17
    s = Student("S001", outstanding_dues=-1)
    c = Course("CS201", 3, 30)
    with pytest.raises(ValueError) as e:
        registration_decision(s, c)
    assert str(e.value) == "Invalid dues"


def test_ecp05_all_prerequisites_done():
    s = Student("S001", completed_courses={"CS101", "MATH101"})
    c = Course("CS201", 3, 30, prerequisites={"CS101", "MATH101"})
    assert registration_decision(s, c) == "REGISTERED"


def test_ecp06_some_prerequisites_done():
    # same as acceptance scenario 3
    s = Student("S001", completed_courses={"CS101"})
    c = Course("CS201", 3, 30, prerequisites={"CS101", "MATH101"})
    assert registration_decision(s, c) == "PREREQUISITES_MISSING"


def test_ecp07_no_prerequisite_done():
    s = Student("S001", completed_courses={"HIST100"})
    c = Course("CS201", 3, 30, prerequisites={"CS101", "MATH101"})
    assert registration_decision(s, c) == "PREREQUISITES_MISSING"


def test_ecp08_already_registered():
    s = Student("S001", registered_courses={"CS201"})
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "ALREADY_REGISTERED"


def test_ecp10_course_full():
    # same as bva12, dt05, acceptance scenario 5
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=30)
    assert registration_decision(s, c) == "WAITLISTED"


def test_ecp11_course_credits_0():
    # same as bva06
    s = Student("S001")
    c = Course("CS201", 0, 30)
    with pytest.raises(ValueError) as e:
        registration_decision(s, c)
    assert str(e.value) == "Invalid course credits"


def test_ecp12_course_credits_5():
    # same as bva07
    s = Student("S001")
    c = Course("CS201", 5, 30)
    with pytest.raises(ValueError) as e:
        registration_decision(s, c)
    assert str(e.value) == "Invalid course credits"


def test_ecp13_capacity_0():
    s = Student("S001")
    c = Course("CS201", 3, 0)
    with pytest.raises(ValueError) as e:
        registration_decision(s, c)
    assert str(e.value) == "Invalid capacity or enrollment"


def test_ecp14_enrolled_more_than_capacity():
    # same as bva13
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=31)
    with pytest.raises(ValueError) as e:
        registration_decision(s, c)
    assert str(e.value) == "Invalid capacity or enrollment"


def test_ecp15_current_credits_19():
    s = Student("S001", current_credits=19)
    c = Course("CS201", 3, 30)
    with pytest.raises(ValueError) as e:
        registration_decision(s, c)
    assert str(e.value) == "Invalid current credits"


def test_ecp16_credit_limit_ok():
    assert check_credit_limit(10, 2) == True


def test_ecp18_no_prerequisites_needed():
    assert prerequisites_satisfied(set(), set()) == True


def test_ecp20_all_prerequisites_completed():
    assert prerequisites_satisfied({"CS101", "MATH101", "X"}, {"CS101", "MATH101"}) == True


def test_ecp21_some_prerequisites_completed():
    assert prerequisites_satisfied({"CS101"}, {"CS101", "MATH101"}) == False


def test_ecp22_nothing_completed():
    assert prerequisites_satisfied(set(), {"CS101"}) == False


# ---------- BVA ----------

def test_bva01_0_plus_1():
    assert check_credit_limit(0, 1) == True


def test_bva04_0_plus_4():
    assert check_credit_limit(0, 4) == True


def test_bva23_14_plus_4_is_18():
    assert check_credit_limit(14, 4) == True


def test_bva24_17_plus_1_is_18():
    assert check_credit_limit(17, 1) == True


def test_bva25_15_plus_3_is_18():
    # same as bva08 and acceptance scenario 1
    assert check_credit_limit(15, 3) == True


def test_bva26_18_plus_1_is_19():
    # same as bva03 and bva19
    assert check_credit_limit(18, 1) == False


def test_bva27_15_plus_4_is_19():
    assert check_credit_limit(15, 4) == False


def test_bva28_16_plus_3_is_19():
    # same as bva09 and acceptance scenario 2
    assert check_credit_limit(16, 3) == False


def test_bva29_current_credits_minus1():
    with pytest.raises(ValueError) as e:
        check_credit_limit(-1, 1)
    assert str(e.value) == "Invalid current credits"


def test_bva30_current_credits_19():
    with pytest.raises(ValueError) as e:
        check_credit_limit(19, 1)
    assert str(e.value) == "Invalid current credits"


def test_bva31_course_credits_0():
    with pytest.raises(ValueError) as e:
        check_credit_limit(0, 0)
    assert str(e.value) == "Invalid course credits"


def test_bva32_course_credits_5():
    with pytest.raises(ValueError) as e:
        check_credit_limit(0, 5)
    assert str(e.value) == "Invalid course credits"


def test_bva33_both_credits_wrong_current_checked_first():
    with pytest.raises(ValueError) as e:
        check_credit_limit(19, 0)
    assert str(e.value) == "Invalid current credits"


def test_bva11_one_seat_left():
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=29)
    assert registration_decision(s, c) == "REGISTERED"


def test_bva14_enrolled_minus1():
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=-1)
    with pytest.raises(ValueError) as e:
        registration_decision(s, c)
    assert str(e.value) == "Invalid capacity or enrollment"


def test_bva16_dues_1():
    # same as acceptance scenario 4
    s = Student("S001", outstanding_dues=1)
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "DUES_BLOCK"


def test_bva18_capacity_1_empty():
    s = Student("S001")
    c = Course("CS201", 3, 1, enrolled=0)
    assert registration_decision(s, c) == "REGISTERED"


def test_bva21_capacity_1_full():
    s = Student("S001")
    c = Course("CS201", 3, 1, enrolled=1)
    assert registration_decision(s, c) == "WAITLISTED"


def test_bva34_registration_total_18():
    s = Student("S001", current_credits=15)
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "REGISTERED"


def test_bva35_registration_total_19():
    s = Student("S001", current_credits=16)
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "CREDIT_LIMIT"


# ---------- Decision table (order: dues, registered, prereq, credit, full) ----------

def test_dt01_dues_first():
    s = Student("S001", outstanding_dues=1, registered_courses={"CS201"}, current_credits=18)
    c = Course("CS201", 3, 30, enrolled=30, prerequisites={"X1"})
    assert registration_decision(s, c) == "DUES_BLOCK"


def test_dt02_registered_second():
    s = Student("S001", registered_courses={"CS201"}, current_credits=18)
    c = Course("CS201", 3, 30, enrolled=30, prerequisites={"X1"})
    assert registration_decision(s, c) == "ALREADY_REGISTERED"


def test_dt03_prerequisite_third():
    s = Student("S001", current_credits=18)
    c = Course("CS201", 3, 30, enrolled=30, prerequisites={"X1"})
    assert registration_decision(s, c) == "PREREQUISITES_MISSING"


def test_dt04_credit_fourth():
    s = Student("S001", current_credits=18)
    c = Course("CS201", 3, 30, enrolled=30)
    assert registration_decision(s, c) == "CREDIT_LIMIT"


def test_dt07_dues_and_registered():
    s = Student("S001", outstanding_dues=1, registered_courses={"CS201"})
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "DUES_BLOCK"


def test_dt08_registered_and_prerequisite():
    s = Student("S001", registered_courses={"CS201"})
    c = Course("CS201", 3, 30, prerequisites={"X1"})
    assert registration_decision(s, c) == "ALREADY_REGISTERED"


def test_dt09_prerequisite_and_credit():
    s = Student("S001", current_credits=18)
    c = Course("CS201", 3, 30, prerequisites={"X1"})
    assert registration_decision(s, c) == "PREREQUISITES_MISSING"


def test_dt10_credit_and_full():
    s = Student("S001", current_credits=16)
    c = Course("CS201", 3, 30, enrolled=30)
    assert registration_decision(s, c) == "CREDIT_LIMIT"


def test_dt11_dues_error_before_capacity_error():
    s = Student("S001", outstanding_dues=-1)
    c = Course("CS201", 3, 0)
    with pytest.raises(ValueError) as e:
        registration_decision(s, c)
    assert str(e.value) == "Invalid dues"


# ---------- State changes ----------

def test_decision_does_not_change_anything():
    s = Student("S001")
    c = Course("CS201", 3, 30)
    registration_decision(s, c)
    assert s.registered_courses == set()
    assert s.current_credits == 0
    assert c.enrolled == 0


def test_register_success():
    s = Student("S001", current_credits=6)
    c = Course("CS201", 3, 30, enrolled=5)
    result = register_course(s, c)
    assert result == "REGISTERED"
    assert "CS201" in s.registered_courses
    assert s.current_credits == 9
    assert c.enrolled == 6


def test_waitlist_adds_student():
    s = Student("S001", current_credits=6)
    c = Course("CS201", 3, 30, enrolled=30)
    result = register_course(s, c)
    assert result == "WAITLISTED"
    assert c.waitlist == ["S001"]
    assert s.registered_courses == set()
    assert s.current_credits == 6
    assert c.enrolled == 30


def test_waitlist_no_duplicate():
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=30, waitlist=["S001"])
    result = register_course(s, c)
    assert result == "WAITLISTED"
    assert c.waitlist == ["S001"]


def test_failed_dues_no_change():
    s = Student("S001", outstanding_dues=1)
    c = Course("CS201", 3, 30)
    result = register_course(s, c)
    assert result == "DUES_BLOCK"
    assert s.registered_courses == set()
    assert s.current_credits == 0
    assert c.enrolled == 0


def test_failed_already_registered_no_change():
    s = Student("S001", registered_courses={"CS201"}, current_credits=3)
    c = Course("CS201", 3, 30, enrolled=1)
    result = register_course(s, c)
    assert result == "ALREADY_REGISTERED"
    assert s.current_credits == 3
    assert c.enrolled == 1


def test_failed_prerequisite_no_change():
    s = Student("S001")
    c = Course("CS201", 3, 30, prerequisites={"CS101"})
    result = register_course(s, c)
    assert result == "PREREQUISITES_MISSING"
    assert s.registered_courses == set()
    assert c.enrolled == 0


def test_failed_credit_limit_no_change():
    s = Student("S001", current_credits=16)
    c = Course("CS201", 3, 30)
    result = register_course(s, c)
    assert result == "CREDIT_LIMIT"
    assert s.current_credits == 16
    assert c.enrolled == 0


def test_register_twice():
    s = Student("S001")
    c = Course("CS201", 3, 30)
    assert register_course(s, c) == "REGISTERED"
    assert register_course(s, c) == "ALREADY_REGISTERED"
    assert s.current_credits == 3
    assert c.enrolled == 1


def test_withdraw_success():
    # acceptance scenario 6
    s = Student("S001", current_credits=9, registered_courses={"CS201", "CS101"})
    c = Course("CS201", 3, 30, enrolled=10)
    result = withdraw_course(s, c)
    assert result == True
    assert s.registered_courses == {"CS101"}
    assert s.current_credits == 6
    assert c.enrolled == 9


def test_withdraw_not_registered():
    s = Student("S001", current_credits=3, registered_courses={"CS101"})
    c = Course("CS201", 3, 30, enrolled=4)
    result = withdraw_course(s, c)
    assert result == False
    assert s.current_credits == 3
    assert s.registered_courses == {"CS101"}
    assert c.enrolled == 4


def test_register_then_withdraw():
    s = Student("S001")
    c = Course("CS201", 3, 30)
    register_course(s, c)
    result = withdraw_course(s, c)
    assert result == True
    assert s.current_credits == 0
    assert c.enrolled == 0
    assert s.registered_courses == set()
