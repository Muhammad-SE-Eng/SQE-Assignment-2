import sys; sys.path.insert(0, '.'); sys.path.insert(0, 'tests')
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

ss = getSampleStyleSheet()
B = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13)
SM = ParagraphStyle("sm", parent=B, fontSize=8, leading=10)
H1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, spaceBefore=10)
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=11.5, spaceBefore=8)
def P(t, s=B): return Paragraph(t, s)
def table(data, widths, hdr=True, fs=8):
    data = [[P(str(c), SM) for c in r] for r in data]
    t = Table(data, colWidths=widths, repeatRows=1 if hdr else 0)
    st = [("GRID", (0,0), (-1,-1), 0.4, colors.grey), ("VALIGN", (0,0), (-1,-1), "TOP")]
    if hdr: st += [("BACKGROUND", (0,0), (-1,0), colors.HexColor("#D9E2F3"))]
    t.setStyle(TableStyle(st)); return t


s = []
s += [P("SE3002 - Software Quality Engineering", H1), P("<b>Assignment 2: Final Testing Report</b> - Student Course Registration System"),
      P("GitHub repository: https://github.com/Muhammad-SE-Eng/SQE-Assignment-2<br/>Contributors and reviews: See merged pull requests."), Spacer(1,6)]

s += [P("1. Black-box design: ECP, BVA, decision table, optimization", H1),
      P("We wrote the expected results from REQUIREMENTS.md (FR-01 to FR-15) before looking at registration.py. The black-box file tests/test_blackbox.py has 18 ECP tests, 20 BVA tests and 9 decision table tests, plus tests for registration and withdrawal state changes (59 tests in total). The design sheets are in docs/blackbox_test_design.xlsx and docs/decision_table.xlsx."),
      P("<b>ECP:</b> dues (zero, positive, negative), prerequisites (none, all, some, none completed), already registered, seats free or full, course credits valid or invalid, current credits invalid, capacity/enrolled invalid. <b>BVA:</b> current credits 0, 18 (and -1, 19); course credits 1, 4 (and 0, 5); total credits 18 vs 19 (14+4, 15+3, 17+1 vs 15+4, 16+3, 18+1); enrolled = capacity-1, capacity, capacity+1, -1; capacity 0 and 1; dues -1, 0, 1."),
      Spacer(1,4),
      table([["Rule","C1 dues&gt;0","C2 already reg.","C3 prereq missing","C4 credit &gt;18","C5 full","Outcome"],
             ["DT-01","T","-","-","-","-","DUES_BLOCK"],["DT-02","F","T","-","-","-","ALREADY_REGISTERED"],
             ["DT-03","F","F","T","-","-","PREREQUISITES_MISSING"],["DT-04","F","F","F","T","-","CREDIT_LIMIT"],
             ["DT-05","F","F","F","F","T","WAITLISTED"],["DT-06","F","F","F","F","F","REGISTERED"]],
            [1.4*cm,2.1*cm,2.6*cm,3*cm,2.6*cm,1.6*cm,4.2*cm]),
      P("Priority combinations (all conditions below the first applicable one set to True) are tested by DT-01 to DT-04 and by DT-07 (dues+registered), DT-08 (registered+prereq), DT-09 (prereq+credit), DT-10 (credit+full) and DT-11 (invalid dues checked before invalid capacity).", SM),
      P("<b>Optimization (A5).</b> A case was written only once when two techniques used exactly the same input and expected result. For example the normal eligible student is ECP-01, ECP-04, ECP-09, BVA-15 and DT-06 together, and the full course is ECP-10, BVA-12, DT-05 and AC-05. Cases with the same output but different input (dues 500 and dues 1) were kept separate. Each technique id is still written in the test comment so it can be traced.")]

s += [PageBreak(), P("2. White-box analysis of registration_decision()", H1),
      Image("docs/cfg.png", width=9.5*cm, height=14.2*cm),
      P("<b>Cyclomatic complexity.</b> N = 17 (Start, 7 decision nodes, 8 return/raise nodes, Exit), E = 23, so V(G) = E - N + 2 = <b>8</b>. "
        "Method A (each compound predicate = one decision node): 7 decisions + 1 = 8, matching V(G). "
        "Method B (each atomic condition of the compound predicate d2 counted separately, chained comparison = 2 atoms): 9 decisions + 1 = 10; V(G) of the condition-level graph is also 10."),
      P("<b>Independent basis paths (8).</b> P1 d1=T; P2 d1=F,d2=T; P3 d3=T; P4 d4=T; P5 d5=T; P6 d6=T; P7 d7=T (WAITLISTED); P8 all False (REGISTERED). Tests: test_path1 to test_path8. P7 is <b>infeasible in the supplied code</b> because d2 guarantees enrolled &lt;= capacity; this is defect D4. After the fix (&gt;=) P7 is feasible and tested by test_ecp10."),
      Spacer(1,4), P("<b>MC/DC</b> for d2 = not(a and b) or c, with a: 0 &lt;= enrolled, b: enrolled &lt;= capacity, c: capacity &lt; 1 (N = not evaluated, due to Python short-circuiting):", B),
      table([["Test","a","b","c","D","(enrolled, capacity)"],["MCDC-1","F","N","N","T","(-1, 30)"],["MCDC-2","T","F","N","T","(31, 30)"],
             ["MCDC-3","T","T","F","F","(5, 30)"],["MCDC-4","T","T","T","T","(0, 0)"]],[2.5*cm,1.5*cm,1.5*cm,1.5*cm,1.5*cm,4*cm]),
      P("Independent-effect pairs: a - (MCDC-1, MCDC-3); b - (MCDC-2, MCDC-3); c - (MCDC-3, MCDC-4). Four tests (n+1) achieve MC/DC. "
        "Condition coverage on the other predicates is trivial (single atomic conditions). pytest-cov does not measure condition coverage or MC/DC, so these were calculated manually.", B)]

s += [P("3. Coverage before and after white-box additions", H1),
      table([["Stage","Tests","Statements","Branch","Total cover","Uncovered"],
             ["Initial (black-box only, original code)","59 (42 pass, 17 fail)","57, miss 3","26, partial 3","93%","line 51 (DUES_BLOCK return), 59 (WAITLISTED return), 71 (waitlist append)"],
             ["Final (+ white-box, original code)","76 (58 pass, 18 fail)","57, miss 2","26, partial 2","95%","lines 59 and 71 - cannot be reached because of D4"],
             ["After defect fixes (regression)","76 (76 pass)","54, miss 0","26, partial 0","100%","none"]],
            [4.2*cm,2.6*cm,2*cm,2*cm,1.8*cm,4.6*cm]),
      P("Tests added in test_whitebox.py: test_wb01 (dues over 1000, covers line 51), test_wb02 (dues = 1000), test_wb03 to test_wb06 (other branches of register_course, check_credit_limit, prerequisites_satisfied and withdraw_course), test_path1 to test_path8 and test_mcdc1 to test_mcdc4. Lines 59 and 71 (WAITLISTED return and adding to the waitlist) cannot be covered with the given code because of defect D4, so we did not force them; after the fix they are covered by the black-box tests (100%). Line 51 was missed at first only because no black-box test used dues above 1000. Even the first 93% found all 5 defects, so a high coverage number does not mean the code is correct."), Spacer(1,4)]

s += [P("4. Defects and fix status", H1),
      table([["ID","Requirement","Defect","Failing tests","Issue / status"],
             ["D1","FR-01, FR-07","check_credit_limit uses &lt; 18 (total of 18 rejected)","bva23, bva24, bva25, bva34","Fixed (PR #8)"],
             ["D2","FR-03, FR-06","prerequisites checked with intersection (any) not all","ecp21, ecp06","Fixed (PR #8)"],
             ["D3","FR-04","dues block only when &gt; 1000; must be &gt; 0","ecp02, bva16, dt01, dt07, failed_dues_no_change, wb02","Fixed (PR #8)"],
             ["D4","FR-08, FR-12","waitlist test enrolled &gt; capacity unreachable; full course returns REGISTERED","ecp10, bva21, waitlist_adds_student, waitlist_no_duplicate","Fixed (PR #8)"],
             ["D5","FR-13","withdraw_course does not decrement course.enrolled","withdraw_success, register_then_withdraw","Fixed (PR #8)"]],
            [1*cm,2.2*cm,5*cm,5.3*cm,3.7*cm]),
      P("Initial failing runs were saved (evidence/blackbox_initial_run.txt, evidence/coverage_initial.txt, and the first GitHub Actions run) before any fix. Fixes are on the defect-fixes branch; after the fixes all 76 tests pass. Expected values were never edited to match the code.", B)]

s += [P("5. Repository, pull requests and contributions", H1),
      table([["Item","Link / detail"],["Repository","https://github.com/Muhammad-SE-Eng/SQE-Assignment-2"],["PR #1 blackbox-testing","https://github.com/Muhammad-SE-Eng/SQE-Assignment-2/pull/1"],["PR #7 whitebox-testing","https://github.com/Muhammad-SE-Eng/SQE-Assignment-2/pull/7"],
             ["PR #8 defect-fixes","https://github.com/Muhammad-SE-Eng/SQE-Assignment-2/pull/8"],["GitHub Actions: failing run before fixes","See repository Actions tab"],["GitHub Actions: passing run after fixes","See repository Actions tab"]],[6*cm,10*cm]),
      Spacer(1,6),
      table([["Member","Contribution"],
             ["Ghulam Muhammad (24P-3116)","Black-box and white-box testing, defect fixes, regression testing and final report."],
             ["Vinod Kumar (24P-3012)","Group member; collaborative work on the Student Course Registration System."]],
            [5*cm,11*cm])]

SimpleDocTemplate("docs/testing_report.pdf", pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
                  title="SE3002 Assignment 2 - Testing Report").build(s)
print("done")
