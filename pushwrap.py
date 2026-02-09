#!/usr/bin/env python3
import argparse
import subprocess
import sys
import time
import os
import requests
import shlex


SIMPLEPUSH_URL = "https://simplepu.sh"


def send_simplepush(key, title, msg, event):
    payload = {
        "key": key,
        "title": title,
        "msg": msg,
        "event": event
    }

    try:
        r = requests.post(SIMPLEPUSH_URL, json=payload, timeout=10)
        return r.status_code == 200
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Run any command and send Simplepush notification when finished"
    )

    parser.add_argument(
        "--push-key",
        help="Simplepush key (or via SIMPLEPUSH_KEY env var)"
    )
    parser.add_argument(
        "--min-seconds",
        type=int,
        default=0,
        help="Only send push if runtime >= this value"
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Disable push (dry wrapper run)"
    )
    parser.add_argument(
        "--title-success",
        default="Command finished",
        help="Push title on success"
    )
    parser.add_argument(
        "--title-failure",
        default="Command error",
        help="Push title on failure"
    )

    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run (use -- before command)"
    )

    args = parser.parse_args()

    if not args.command or args.command[0] != "--":
        print("[!] You must separate command with --", file=sys.stderr)
        sys.exit(2)

    cmd = args.command[1:]

    if not cmd:
        print("[!] No command specified", file=sys.stderr)
        sys.exit(2)

    push_key = args.push_key or os.getenv("SIMPLEPUSH_KEY")

    if not args.no_push and not push_key:
        print("[!] No Simplepush key provided (use --push-key or SIMPLEPUSH_KEY)", file=sys.stderr)
        sys.exit(2)

    start = time.time()

    try:
        proc = subprocess.Popen(cmd)
        rc = proc.wait()
    except KeyboardInterrupt:
        rc = 130
    except FileNotFoundError:
        print(f"[!] Command not found: {cmd[0]}", file=sys.stderr)
        sys.exit(127)

    duration = int(time.time() - start)

    if args.no_push or duration < args.min_seconds:
        sys.exit(rc)

    cmd_str = shlex.join(cmd)

    if rc == 0:
        title = args.title_success
        event = "success"
        msg = f"{cmd_str}\nDuration: {duration}s"
    else:
        title = args.title_failure
        event = "error"
        msg = f"{cmd_str}\nExit-Code: {rc}\nDuration: {duration}s"

    send_simplepush(push_key, title, msg, event)

    sys.exit(rc)


if __name__ == "__main__":
    main()