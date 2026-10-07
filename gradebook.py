# gradebook.py -- the department gradebook service

import http.server
import json
import logging
import sys
from collections.abc import Callable
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from errors import ConflictError, GradebookError, NotFoundError, ValidationError
from models import parse_assessment, parse_mark, parse_student

DATA = "gradebook.json"

STATE: dict[str, Any] = {
    "students": {},
    "assessments": {},
    "marks": [],
}

logger = logging.getLogger(__name__)


def load() -> None:
    global STATE

    try:
        with open(DATA, "r") as f:
            STATE = json.load(f)
    except FileNotFoundError:
        STATE = {
            "students": {},
            "assessments": {},
            "marks": [],
        }


def save() -> None:
    with open(DATA, "w") as f:
        json.dump(STATE, f, indent=2)


def pct(sid: str) -> str:
    total = 0.0
    got = 0.0

    for mark in STATE["marks"]:
        if mark.get("student") != sid:
            continue

        assessment_id = mark.get("assessment")
        assessment = STATE["assessments"].get(assessment_id)

        if not assessment:
            continue

        try:
            score = float(mark.get("score", 0))
            weight = float(assessment.get("weight", 0))
            assessment_total = float(assessment.get("total", 100))
        except (ValueError, TypeError):
            continue

        if assessment_total == 0:
            continue

        got += score * weight / assessment_total
        total += weight

    if total == 0:
        return "0"

    return str(round(got, 2))


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        logger.info(
            "%s - %s",
            self.address_string(),
            format % args,
        )

    def _send(self, code: int, obj: object) -> None:
        body = json.dumps(obj).encode()

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def _run(
        self,
        operation: Callable[[], tuple[int, object]],
    ) -> None:
        try:
            status, body = operation()
            self._send(status, body)

        except ValidationError as exc:
            self._send(400, {"error": str(exc)})

        except NotFoundError as exc:
            self._send(404, {"error": str(exc)})

        except ConflictError as exc:
            self._send(409, {"error": str(exc)})

        except GradebookError as exc:
            self._send(400, {"error": str(exc)})

        except Exception:
            logger.exception("unexpected error")
            self._send(500, {"error": "internal error"})

    def _read_json(self) -> object:
        content_length = self.headers.get("Content-Length", "0")

        try:
            length = int(content_length)
        except ValueError as exc:
            raise ValidationError(
                "Content-Length must be a valid number."
            ) from exc

        raw = self.rfile.read(length)

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValidationError("Invalid JSON.") from exc

    # GET operations

    def get_students(self) -> tuple[int, object]:
        return 200, list(STATE["students"].values())

    def get_student(self, sid: str) -> tuple[int, object]:
        if sid not in STATE["students"]:
            raise NotFoundError("Student not found.")

        student = dict(STATE["students"][sid])
        student["percentage"] = pct(sid)

        return 200, student

    def get_assessments(self) -> tuple[int, object]:
        return 200, list(STATE["assessments"].values())

    def get_report(self) -> tuple[int, object]:
        report = []

        for sid in STATE["students"]:
            report.append(
                {
                    "id": sid,
                    "name": STATE["students"][sid]["name"],
                    "pct": pct(sid),
                }
            )

        return 200, report

    # POST operations

    def create_student(self, payload: object) -> tuple[int, object]:
        student = parse_student(payload)

        if student.id in STATE["students"]:
            raise ConflictError("Student already exists.")

        record = asdict(student)
        record["joined"] = str(datetime.now(timezone.utc))

        STATE["students"][student.id] = record
        save()

        return 200, record

    def create_assessment(self, payload: object) -> tuple[int, object]:
        assessment = parse_assessment(payload)

        if assessment.id in STATE["assessments"]:
            raise ConflictError("Assessment already exists.")

        record = asdict(assessment)

        STATE["assessments"][assessment.id] = record
        save()

        return 200, record

    def create_mark(self, payload: object) -> tuple[int, object]:
        mark = parse_mark(payload)

        if mark.student not in STATE["students"]:
            raise NotFoundError("Student not found.")

        if mark.assessment not in STATE["assessments"]:
            raise NotFoundError("Assessment not found.")

        assessment = STATE["assessments"][mark.assessment]
        assessment_total = float(assessment["total"])

        if mark.score > assessment_total:
            raise ValidationError(
                "score must not be greater than assessment total."
            )

        record = asdict(mark)
        record["at"] = str(datetime.now(timezone.utc))

        STATE["marks"].append(record)
        save()

        logger.info(
            "recorded mark for %s score %s",
            mark.student,
            mark.score,
        )

        return 200, {"ok": True}

    def post_request(self) -> tuple[int, object]:
        payload = self._read_json()

        if self.path == "/students":
            return self.create_student(payload)

        if self.path == "/assessments":
            return self.create_assessment(payload)

        if self.path == "/marks":
            return self.create_mark(payload)

        raise NotFoundError("Unknown endpoint.")

    # HTTP methods

    def do_GET(self) -> None:
        if self.path == "/students":
            self._run(self.get_students)

        elif self.path.startswith("/students/"):
            sid = self.path.split("/")[2]
            self._run(lambda: self.get_student(sid))

        elif self.path == "/assessments":
            self._run(self.get_assessments)

        elif self.path == "/report":
            self._run(self.get_report)

        else:
            self._run(
                lambda: self._raise_not_found("Unknown endpoint.")
            )

    def do_POST(self) -> None:
        self._run(self.post_request)

    @staticmethod
    def _raise_not_found(message: str) -> tuple[int, object]:
        raise NotFoundError(message)


def main(argv: list[str] = sys.argv) -> None:
    load()

    port = 8000

    if len(argv) > 1:
        port = int(argv[1])

    logger.info("gradebook on %s", port)

    http.server.HTTPServer(
        ("", port),
        Handler,
    ).serve_forever()


if __name__ == "__main__":
    main()