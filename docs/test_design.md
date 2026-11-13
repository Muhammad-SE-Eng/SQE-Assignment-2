# Test design notes

Defects found by the black-box tests (17 failing tests + test_wb02):
D1 credit limit uses `< 18` instead of `<= 18` | D2 prerequisites use "any" instead of "all" |
D3 dues block only above 1000 instead of above 0 | D4 full course never gets WAITLISTED (`>` instead of `>=`) |
D5 withdraw_course does not reduce course.enrolled.

CFG: N=17, E=23, V(G)=E-N+2=8 (7 decisions + 1). Counting each atomic condition of the
compound decision separately gives 10. See docs/cfg.png.

MC/DC for `not (0 <= enrolled <= capacity) or capacity < 1`: 4 tests (mcdc1-mcdc4) in test_whitebox.py.

Coverage: 93% (black-box only) -> 95% (with white-box) -> 100% after fixes.
Lines 59 and 71 cannot be reached before the fix because of D4.
