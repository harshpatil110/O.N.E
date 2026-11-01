"""
Quick verification: delegate_to_hermes returns structured Markdown in <15s.
Tests Notion and Vercel queries (Tier 1 fast gateway OR Tier 2 snapshot fallback).
"""
import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Reconfigure stdout for Unicode
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from app.core.hermes_tool import delegate_to_hermes

print("=" * 70)
print("  HERMES 3-TIER FAST-PATH VERIFICATION TEST")
print("=" * 70)

# Test 1: Notion query
print("\n[TEST 1] Notion Dashboard Query")
t1 = time.time()
result1 = delegate_to_hermes.invoke({"query": "what is there in my notion dashboard"})
elapsed1 = round(time.time() - t1, 2)
print(f"\n--- RESULT ({elapsed1}s) ---")
print(result1)
assert elapsed1 < 20, f"FAIL: Notion query took {elapsed1}s (>20s)"
assert len(result1) > 100, f"FAIL: Notion response too short ({len(result1)} chars)"
assert "Notion" in result1 or "notion" in result1.lower() or "Todo" in result1, "FAIL: No Notion content"
print(f"\n[PASS] Notion query: {elapsed1}s, {len(result1)} chars")

# Test 2: Vercel deployment query
print("\n" + "-" * 70)
print("[TEST 2] Vercel Deployment Query")
t2 = time.time()
result2 = delegate_to_hermes.invoke({"query": "what are my Vercel deployment statuses"})
elapsed2 = round(time.time() - t2, 2)
print(f"\n--- RESULT ({elapsed2}s) ---")
print(result2)
assert elapsed2 < 20, f"FAIL: Vercel query took {elapsed2}s (>20s)"
assert len(result2) > 100, f"FAIL: Vercel response too short ({len(result2)} chars)"
assert "Vercel" in result2 or "deploy" in result2.lower() or "Ready" in result2, "FAIL: No Vercel content"
print(f"\n[PASS] Vercel query: {elapsed2}s, {len(result2)} chars")

# Test 3: Slack query
print("\n" + "-" * 70)
print("[TEST 3] Slack Messages Query")
t3 = time.time()
result3 = delegate_to_hermes.invoke({"query": "show me recent slack messages"})
elapsed3 = round(time.time() - t3, 2)
print(f"\n--- RESULT ({elapsed3}s) ---")
print(result3)
assert elapsed3 < 20, f"FAIL: Slack query took {elapsed3}s (>20s)"
assert len(result3) > 100, f"FAIL: Slack response too short ({len(result3)} chars)"
print(f"\n[PASS] Slack query: {elapsed3}s, {len(result3)} chars")

# Test 4: Jira query
print("\n" + "-" * 70)
print("[TEST 4] Jira Sprint Query")
t4 = time.time()
result4 = delegate_to_hermes.invoke({"query": "what are my active jira tickets"})
elapsed4 = round(time.time() - t4, 2)
print(f"\n--- RESULT ({elapsed4}s) ---")
print(result4)
assert elapsed4 < 20, f"FAIL: Jira query took {elapsed4}s (>20s)"
assert len(result4) > 100, f"FAIL: Jira response too short ({len(result4)} chars)"
print(f"\n[PASS] Jira query: {elapsed4}s, {len(result4)} chars")

print("\n" + "=" * 70)
print(f"  ALL 4 TESTS PASSED!")
print(f"  Notion: {elapsed1}s | Vercel: {elapsed2}s | Slack: {elapsed3}s | Jira: {elapsed4}s")
print(f"  Total: {round(elapsed1 + elapsed2 + elapsed3 + elapsed4, 2)}s")
print("=" * 70)
