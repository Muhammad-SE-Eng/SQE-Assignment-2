# White-box tests, written after reading registration.py.
# Expected results still come from REQUIREMENTS.md.
# The comment above each test says which branch / condition / path it covers.

import pytest
from registration import Student, Course
from registration import check_credit_limit, prerequisites_satisfied
from registration import registration_decision, register_course, withdraw_course


# ---------- tests for lines/branches the black-box tests missed ----------

def test_wb01_dues_over_1000():
    # branch: dues > 1000 is True (return DUES_BLOCK)
    s = Student("S001", outstanding_dues=1001)
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "DUES_BLOCK"


def test_wb02_dues_exactly_1000():
    # boundary of the dues > 1000 condition. SRS says any dues above 0 blocks
    s = Student("S001", outstanding_dues=1000)
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "DUES_BLOCK"


def test_wb03_register_other_outcome():
    # register_course: decision is not REGISTERED and not WAITLISTED
    s = Student("S001", registered_courses={"CS201"}, current_credits=3)
    c = Course("CS201", 3, 30)
    assert register_course(s, c) == "ALREADY_REGISTERED"
    assert s.current_credits == 3
    assert c.waitlist == []


def test_wb04_check_credit_limit_branches():
    # both error branches and the normal return
    with pytest.raises(ValueError):
        check_credit_limit(-1, 1)
    with pytest.raises(ValueError):
        check_credit_limit(0, 5)
    assert check_credit_limit(0, 1) == True


def test_wb05_prerequisites_branches():
    # "if not required" True and then False
    assert prerequisites_satisfied(set(), set()) == True
    assert prerequisites_satisfied({"A"}, {"A"}) == True


def test_wb06_withdraw_both_branches():
    # withdraw_course: registered (True) then not registered (False)
    s = Student("S001", current_credits=3, registered_courses={"CS201"})
    c = Course("CS201", 3, 30)
    assert withdraw_course(s, c) == True
    assert withdraw_course(s, c) == False

# NOTE: the lines "return WAITLISTED" (line 59) and the waitlist append in
# register_course (line 71) can not be reached with the given code because
# of defect D4 (enrolled > capacity can never be true). They are only
# reached after the fix, by test_ecp10 and test_waitlist_adds_student.


# ---------- basis paths of registration_decision (V(G) = 8) ----------
# path 7 (WAITLISTED) is not possible with the given code (see note above)

def test_path1_negative_dues():
    s = Student("S001", outstanding_dues=-5)
    c = Course("CS201", 3, 30)
    with pytest.raises(ValueError):
        registration_decision(s, c)


def test_path2_invalid_enrollment():
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=31)
    with pytest.raises(ValueError):
        registration_decision(s, c)


def test_path3_dues_block():
    s = Student("S001", outstanding_dues=2000)
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "DUES_BLOCK"


def test_path4_already_registered():
    s = Student("S001", registered_courses={"CS201"})
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "ALREADY_REGISTERED"


def test_path5_prerequisites_missing():
    s = Student("S001")
    c = Course("CS201", 3, 30, prerequisites={"CS101"})
    assert registration_decision(s, c) == "PREREQUISITES_MISSING"


def test_path6_credit_limit():
    s = Student("S001", current_credits=18)
    c = Course("CS201", 1, 30)
    assert registration_decision(s, c) == "CREDIT_LIMIT"


def test_path8_registered():
    s = Student("S001")
    c = Course("CS201", 3, 30)
    assert registration_decision(s, c) == "REGISTERED"


# ---------- MC/DC ----------
# decision: not (0 <= enrolled <= capacity) or capacity < 1
# a = 0 <= enrolled     b = enrolled <= capacity     c = capacity < 1
# N means not evaluated (python short-circuit)
#
#   test    a  b  c  result   (enrolled, capacity)
#   mcdc1   F  N  N  True     (-1, 30)
#   mcdc2   T  F  N  True     (31, 30)
#   mcdc3   T  T  F  False    (5, 30)
#   mcdc4   T  T  T  True     (0, 0)
#
# a changes result in (mcdc1, mcdc3), b in (mcdc2, mcdc3), c in (mcdc3, mcdc4)

def test_mcdc1():
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=-1)
    with pytest.raises(ValueError):
        registration_decision(s, c)


def test_mcdc2():
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=31)
    with pytest.raises(ValueError):
        registration_decision(s, c)


def test_mcdc3():
    s = Student("S001")
    c = Course("CS201", 3, 30, enrolled=5)
    assert registration_decision(s, c) == "REGISTERED"


def test_mcdc4():
    s = Student("S001")
    c = Course("CS201", 3, 0, enrolled=0)
    with pytest.raises(ValueError):
        registration_decision(s, c)
