"""DeepSeek public web tools; Python 3 standard library only."""

import argparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
import os
from pathlib import Path
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


MISSING_KEY_MESSAGE = (
    "DEEPSEEK_API_KEY is missing. Set DEEPSEEK_API_KEY in your operating system's "
    "user or system environment variables to your DeepSeek API Key, then fully exit "
    "and reopen Codex before retrying. Do not paste the key into chat."
)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward the Authorization header to another endpoint.


def text_argument(value):
    if not value.strip() or len(value) > 128:
        raise argparse.ArgumentTypeError("Expected 1-128 nonblank Unicode characters.")
    return value


def url_argument(value):
    try:
        parts = urllib.parse.urlsplit(value)
        valid = (len(value) <= 8192 and parts.scheme in ("http", "https")
                 and parts.hostname and parts.username is None and parts.password is None
                 and not any(c.isspace() or ord(c) < 32 for c in value))
        _ = parts.port
    except ValueError:
        valid = False
    if not valid:
        raise argparse.ArgumentTypeError("Expected an HTTP(S) URL with host, no credentials, <=8192 characters.")
    return value


def retry_delay(headers, attempt):
    value = headers.get("Retry-After") if headers else None
    if value:
        try:
            return max(0.0, float(value))
        except ValueError:
            try:
                return max(0.0, (parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds())
            except (ValueError, TypeError, OverflowError):
                pass
    return 2 ** attempt


def call_api(operation, body, key, timeout, retries):
    opener = urllib.request.build_opener(NoRedirect())
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            "https://api.deepseek.com/v1/tools/" + operation,
            data=payload,
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with opener.open(req, timeout=timeout) as response:
                data = json.load(response)
            if operation == "search":
                if not isinstance(data, dict) or not isinstance(data.get("results"), list):
                    return {"status": "INVALID_RESPONSE"}
                usable = bool(data["results"])
            else:
                if not isinstance(data, dict) or not isinstance(data.get("content"), str):
                    return {"status": "INVALID_RESPONSE"}
                usable = bool(data["content"].strip())
            return {"status": "PASS" if usable else "EMPTY", "data": data}
        except urllib.error.HTTPError as exc:
            code, headers = exc.code, exc.headers
            exc.close()
            result = {"status": {401: "AUTH_REQUIRED", 402: "INSUFFICIENT_BALANCE",
                                  403: "FETCH_REJECTED" if operation == "fetch" else "HTTP_ERROR",
                                  404: "SOURCE_UNAVAILABLE" if operation == "fetch" else "HTTP_ERROR",
                                  429: "RATE_LIMITED"}.get(code, "HTTP_ERROR"), "http_status": code}
            transient = code in (408, 429) or 500 <= code < 600
            delay = retry_delay(headers, attempt)
        except (urllib.error.URLError, TimeoutError, socket.timeout, OSError):
            result, transient, delay = {"status": "NETWORK_ERROR"}, True, 2 ** attempt
        except (ValueError, UnicodeError):
            return {"status": "INVALID_RESPONSE"}
        if not transient or attempt >= retries:
            return result
        if delay > 60:
            result["retry_after_seconds"] = delay
            return result
        time.sleep(delay)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("check-env", help="Print SET/MISSING only; no network request.")
    search = sub.add_parser("search")
    search.add_argument("query", type=text_argument)
    search.add_argument("--count", type=int, choices=range(1, 51), default=5, metavar="1..50")
    search.add_argument("--need-content", action="store_true")
    search.add_argument("--ori-question", type=text_argument)
    fetch = sub.add_parser("fetch")
    fetch.add_argument("url", type=url_argument)
    for command in (search, fetch):
        command.add_argument("--timeout", type=int, choices=range(1, 61), default=45, metavar="1..60")
        command.add_argument("--retries", type=int, choices=range(3), default=2, metavar="0..2")
        command.add_argument("--output", type=Path, help="Save UTF-8 JSON instead of printing page text.")
    args = parser.parse_args()
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if args.operation == "check-env":
        print("SET" if key else "MISSING")
        return 0 if key else 1
    if args.operation == "search":
        body = {"query": args.query, "count": args.count, "need_content": args.need_content}
        if args.ori_question:
            body["ori_question"] = args.ori_question
    else:
        body = {"url": args.url}
    result = call_api(args.operation, body, key, args.timeout, args.retries) if key else {
        "status": "AUTH_REQUIRED", "message": MISSING_KEY_MESSAGE}
    report = {"provider": "deepseek", "operation": args.operation, "request": body,
              "retrieved_at": datetime.now(timezone.utc).isoformat(), **result}
    # Also redact an accidental echo of the key in a query or provider content.
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    if key:
        encoded = encoded.replace(key, "[REDACTED]")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
        print(json.dumps({"status": result["status"], "output": str(args.output)}, ensure_ascii=False))
    else:
        print(encoded)
    return 0 if result["status"] in ("PASS", "EMPTY") else 1


if __name__ == "__main__":
    sys.exit(main())
