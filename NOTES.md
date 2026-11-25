# Lab 06: Debugging and Regression Tests

| Bug | Cause | Fix | Test |
| --- | --- | --- | --- |

## Previous Lab Notes

### Task 2 - Failure Investigation

#### (a) GET /students/NOPE
- Result: HTTP/1.0 200 OK, {"error": "not found"}
- Problem: A missing student incorrectly returns HTTP 200 instead of 404.

#### (b) POST /students with body 5
- Result: curl: (52) Empty reply from server
- Problem: The server crashes/closes the connection instead of returning a proper 400 response.

#### (c) Invalid mark score "abc"
- Result: HTTP/1.0 200 OK, {"ok": true}
- Then GET /students/S1 -> Empty reply from server.
- Problem: The invalid score "abc" was accepted, causing subsequent calculation failure.

#### (d) Assessment total "0"
- Result: ZeroDivisionError: division by zero
- Problem: The report calculation divides by assessment total, which is zero.

#### (e) Mark for unknown assessment
- Result: Accepted without checking assessment existence.
- Problem: A mark for a non-existent assessment was incorrectly accepted.

### Lab 05 Notes
- Cycle 1 & 2 for ensure_weight_fits: validated weights sum to at most 100.
- Duplicate marks defect resolved: replacing previous mark for same student and assessment.
