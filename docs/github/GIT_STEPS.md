# Git steps (run on your machine)
```bash
cd SQE-Assignment-2            # unzip first
git init -b main && git add registration.py requirements.txt README.md REQUIREMENTS.md .github
git commit -m "Initial: starter code, requirements, CI workflow"
git remote add origin <YOUR_REPO_URL> && git push -u origin main

git checkout -b blackbox-testing
git add tests/test_blackbox.py docs/blackbox_test_design.xlsx docs/decision_table.xlsx evidence/blackbox_initial_run.txt
git commit -m "Add black-box ECP/BVA/decision-table pytest suite and design sheets"
git push -u origin blackbox-testing        # open PR #1; let GitHub Actions run (it FAILS - keep this run as evidence)

git checkout main && git checkout -b whitebox-testing
git add tests/test_whitebox.py docs/cfg.png docs/test_design.md evidence/
git commit -m "Add white-box tests, CFG, MC/DC and coverage evidence"
git push -u origin whitebox-testing        # open PR #2

# open Issues 1-5 from docs/github/ISSUES.md BEFORE fixing
git checkout main && git checkout -b defect-fixes
git apply defect-fixes/defect-fixes.patch  # or copy defect-fixes/registration_fixed.py over registration.py
git commit -am "Fix D1-D5 (closes #1 #2 #3 #4 #5)"
git push -u origin defect-fixes            # open PR #3; Actions should now pass
```
Each member should commit under their own name and review another member's PR (leave a comment, then address it).
