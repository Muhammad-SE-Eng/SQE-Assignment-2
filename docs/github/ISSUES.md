# GitHub Issues (copy each block into a new Issue; labels: bug)

## Issue 1 - D1: Credit total of exactly 18 wrongly rejected
- **Requirement:** FR-01, FR-07 (a total of exactly 18 is allowed)
- **Steps:** `check_credit_limit(15, 3)`  (or register a 3-credit course for a student with 15 credits)
- **Expected:** `True` / `REGISTERED` (total = 18)   **Actual:** `False` / `CREDIT_LIMIT`
- **Cause:** `registration.py` `check_credit_limit` returns `current + new < 18` instead of `<= 18`
- **Failed tests:** `test_bva23`, `test_bva24`, `test_bva25`, `test_bva34_registration_total_18`
- **Status:** Open -> Fixed in PR #3 (defect-fixes)

## Issue 2 - D2: Prerequisites satisfied when only some are completed
- **Requirement:** FR-03, FR-06, Scenario 3 (needs both CS101 and MATH101)
- **Steps:** `prerequisites_satisfied({"CS101"}, {"CS101","MATH101"})`
- **Expected:** `False` / `PREREQUISITES_MISSING`   **Actual:** `True` / `REGISTERED`
- **Cause:** uses `bool(completed.intersection(required))` (any) instead of all (`issubset`)
- **Failed tests:** `test_ecp21`, `test_ecp06`
- **Status:** Open -> Fixed in PR #3

## Issue 3 - D3: Dues below Rs. 1001 do not block registration
- **Requirement:** FR-04, Scenario 4 (any amount > 0 blocks)
- **Steps:** student with `outstanding_dues=1` registers for an eligible course
- **Expected:** `DUES_BLOCK`   **Actual:** `REGISTERED` (state changes: credits, enrollment)
- **Cause:** condition is `outstanding_dues > 1000`; must be `> 0`
- **Failed tests:** `test_ecp02`, `test_bva16`, `test_dt01`, `test_dt07`, `test_failed_dues_no_change`, `test_wb02`
- **Status:** Open -> Fixed in PR #3

## Issue 4 - D4: Full course never produces WAITLISTED
- **Requirement:** FR-08, FR-12, Scenario 5
- **Steps:** capacity 30, enrolled 30, eligible student
- **Expected:** `WAITLISTED`, student ID on waitlist   **Actual:** `REGISTERED`, enrolled becomes 31 (invalid state; next call raises ValueError)
- **Cause:** `course.enrolled > course.capacity` is unreachable after validation (enrolled <= capacity); must be `>=`. Line 59 is dead code.
- **Failed tests:** `test_ecp10`, `test_bva21`, `test_waitlist_adds_student`, `test_waitlist_no_duplicate`
- **Status:** Open -> Fixed in PR #3

## Issue 5 - D5: withdraw_course does not decrement course enrollment
- **Requirement:** FR-13, Scenario 6
- **Steps:** register then withdraw; or withdraw a student from a course with enrolled=10
- **Expected:** `enrolled == 9`   **Actual:** `enrolled == 10`
- **Cause:** missing `course.enrolled -= 1`
- **Failed tests:** `test_withdraw_success`, `test_register_then_withdraw`
- **Status:** Open -> Fixed in PR #3
