# Lab 06: Debugging and Regression Tests

| Bug | Cause | Fix | Test |
| --- | --- | --- | --- |
| A: Opening `/students/S1/` says not found (404) | In commit `a9c3ab9`, `self.path.split("/")[2]` was changed to `self.path.removeprefix("/students/")`, which left trailing slashes (`S1/`) and query parameters (`S1?format=json`) in the extracted ID | Parse student ID ignoring query parameters and trailing slashes: `self.path.removeprefix("/students/").split("?")[0].rstrip("/")` | `tests/test_http.py::test_get_student_handles_trailing_slash_and_query` |
| B: Re-adding assessment after disk failure says it already exists | `add_assessment` inserted the assessment into in-memory state before calling `save()`; when save raised `OSError("disk full")`, state was not rolled back | Catch exception during `save_callback()`, rollback by deleting the assessment from `state["assessments"]`, log warning, and re-raise exception | `tests/test_add_assessment.py::test_failed_save_leaves_no_trace` |
| C: Sending wrong binary file to `POST /students` gives 500 error | `json.loads(raw)` raised `UnicodeDecodeError` on non-UTF-8 byte sequence (`\x80\x81\x82`), but `_read_json` only caught `json.JSONDecodeError`. Traceback bottom line: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte` | Catch `ValueError` in `_read_json` (which covers both `UnicodeDecodeError` and `JSONDecodeError`) and raise `ValidationError` so it returns HTTP 400 | `tests/test_http.py::test_body_that_is_not_utf8_is_a_bad_request` |

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
