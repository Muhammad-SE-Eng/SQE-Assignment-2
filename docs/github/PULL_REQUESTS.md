# Pull requests (adjust numbers to match your repo)

## PR #1  blackbox-testing -> main   (author: Member A, reviewer: Member B)
Adds tests/test_blackbox.py, docs/blackbox_test_design.xlsx, docs/decision_table.xlsx.
Test outcome: 59 tests, 42 pass, 17 FAIL (intentional - genuine defects). Linked: #1 #2 #3 #4 #5.
Do not alter expected values to make the tests pass.

## PR #2  whitebox-testing -> main   (author: Member B, reviewer: Member A)
Adds tests/test_whitebox.py, docs/cfg.png, MC/DC analysis, .github/workflows/tests.yml.
Coverage: 93% -> 95% (statements+branches combined by pytest-cov). Test outcome: 76 tests, 58 pass, 18 fail (same 5 defects).

## PR #3  defect-fixes -> main   (author: Member A or B, reviewer: the other)
Applies defect-fixes/defect-fixes.patch to registration.py (5 one-line fixes).
Test outcome: 76 passed, 100% statement and branch coverage. Closes #1 #2 #3 #4 #5.
