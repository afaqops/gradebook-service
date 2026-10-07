# Task 2 - Failure Investigation

## (a) GET /students/NOPE

Command:

curl.exe -i http://localhost:8000/students/NOPE

Result:

HTTP/1.0 200 OK

{"error": "not found"}

Problem:

A missing student incorrectly returns HTTP 200 instead of 404.

## (b) POST /students with body 5

Command:

curl.exe -i -X POST http://localhost:8000/students -H "Content-Type: application/json" -d "5"

Result:

No HTTP reply.

curl: (52) Empty reply from server

Problem:

The server crashes/closes the connection instead of returning a proper 400 response.

## (c) Invalid mark score "abc"

Created student S1 and assessment A1.

Command:

curl.exe -i -X POST http://localhost:8000/marks -H "Content-Type: application/json" -d "@requests/mark.json"

Result:

HTTP/1.0 200 OK

{"ok": true}

Then:

GET /students/S1

Result:

No HTTP reply.

curl: (52) Empty reply from server

Problem:

The invalid score "abc" was accepted, and the later student request caused a server failure.

## (d) Assessment total "0"

Deleted gradebook.json and restarted the service.

Created S1 and an assessment with total "0".

Added a mark.

GET /report:

Result:

No HTTP reply.

curl: (52) Empty reply from server

Server error:

ZeroDivisionError: division by zero

Problem:

The report calculation divides by the assessment total, which is zero.

Reason gradebook.json was deleted:

To reset the saved state so previous test data would not affect the next failure test.

## (e) Mark for unknown assessment

Deleted gradebook.json and restarted the service.

Created S1.

Command:

curl.exe -i -X POST http://localhost:8000/marks -H "Content-Type: application/json" -d "@requests/unknown-assessment.json"

Result:

HTTP/1.0 200 OK

{"ok": true}

Problem:

A mark for a non-existent assessment was incorrectly accepted instead of returning 404.

## Bare except statements

gradebook.py:19

gradebook.py:28

gradebook.py:84

## Ruff

Command:

ruff check .

Result:

10 errors found.

# Task 8 - Model Parser Tests

Command:

python -m pytest

Result:

All model and parser tests passed successfully.

Tests covered:

- Numeric strings are accepted as numbers.
- Text values are rejected as numbers.
- Boolean values are rejected as numbers.
- NaN is rejected as a number.
- An assessment total of zero is rejected.
- Negative mark scores are rejected.
- Missing required fields are rejected.
- Non-dictionary payloads are rejected.
- Valid assessments are parsed correctly.