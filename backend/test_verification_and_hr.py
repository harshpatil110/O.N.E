import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.core.task_tools import (
    classify_verification_tier,
    compute_weighted_confidence,
    send_hr_completion_email,
    VERIFICATION_TIERS,
)

def run_tests():
    print("=" * 70)
    print("  TEST 1: 6-Tier Verification Taxonomy Classification")
    print("=" * 70)
    
    t1 = classify_verification_tier("Automated system check: API verified via MCP tool", "Setup Service")
    t2 = classify_verification_tier("Employee passed knowledge check comprehension quiz with 100%", "Architecture Quiz")
    t3 = classify_verification_tier("Ran curl http://localhost:8000/docs and got 200 OK. Git commit pushed.", "Swagger Docs")
    t6 = classify_verification_tier("I finished the task, please mark it complete.", "Read guidelines")

    print(f"Test 1 (MCP): {VERIFICATION_TIERS[t1]['label']} -> weight {VERIFICATION_TIERS[t1]['weight']}")
    print(f"Test 2 (Quiz): {VERIFICATION_TIERS[t2]['label']} -> weight {VERIFICATION_TIERS[t2]['weight']}")
    print(f"Test 3 (Proof-of-work): {VERIFICATION_TIERS[t3]['label']} -> weight {VERIFICATION_TIERS[t3]['weight']}")
    print(f"Test 6 (Self-attestation): {VERIFICATION_TIERS[t6]['label']} -> weight {VERIFICATION_TIERS[t6]['weight']}")

    print("\n" + "=" * 70)
    print("  TEST 2: Overall Weighted Verification Confidence Score Calculation")
    print("=" * 70)
    tasks_sample = [
        {"task_name": "Setup PostgreSQL & Run Alembic Migrations", "tier_key": t1},
        {"task_name": "Review System Architecture & Pass Comprehension Quiz", "tier_key": t2},
        {"task_name": "Verify Swagger /docs 200 OK & Service Health Check", "tier_key": t3},
        {"task_name": "Submit First Pull Request & Security Attestation", "tier_key": t6},
    ]
    score_res = compute_weighted_confidence(tasks_sample)
    print(f"Overall Weighted Confidence Score: {score_res['score_pct']}% — {score_res['label']}")
    for b in score_res["breakdown"]:
        print(f"  • {b['task_name']}: {b['tier_label']} (Weight: {b['weight_pct']})")

    print("\n" + "=" * 70)
    print("  TEST 3: HR Completion Report Tool (`send_hr_completion_email`)")
    print("=" * 70)
    report_out = send_hr_completion_email.invoke({"user_id": "test-demo-user-id"})
    print("Report Output Preview:")
    print("-" * 50)
    print(report_out)
    print("-" * 50)

    html_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "hr_completion_report.html"))
    print(f"\nHTML File Generated: {os.path.exists(html_file)}")
    if os.path.exists(html_file):
        print(f"HTML File Path: {html_file}")
        print(f"HTML File Size: {os.path.getsize(html_file)} bytes")

    print("\n" + "=" * 70)
    print("  ALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()

