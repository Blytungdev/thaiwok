#!/usr/bin/env python3

import subprocess
import json
import sys
import os

import gspread

# Config 
CONFIG               = "config.json"

# Private config
with open(CONFIG) as cf:
    config = json.load(cf)
    
SSH_USER        = config["ssh_user"]
SSH_HOST        = config["ssh_host"]
SSH_PATH        = config["ssh_keypath"]
SSH_PORT        = config["ssh_port"]

REMOTE_SCRIPT_PATH = config["remote_script"]

GOOGLE_CREDENTIALS = config["credentials"]
SPREADSHEET_ID  = config["sheet_id"]
WORKSHEET_NAME  = config["worksheet_name"]

def get_measurement_via_ssh() -> dict:
    """
    SSH into the Pi, run the measurement script, and parse its JSON output.
    Returns a dict: {"timestamp": "...", "voltage": ...}
    """


    ssh_command = [
        "ssh",
        "-i",
        SSH_PATH,
        "-p",
        SSH_PORT,
        f"{SSH_USER}@{SSH_HOST}",
        # Make sure the Pi's python3 is on the path:
        "bash", "-lc", f"'uv run {REMOTE_SCRIPT_PATH}'"
    ]

    try:
        completed = subprocess.run(
            ssh_command,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print("ERROR: SSH command failed.", file=sys.stderr)
        print("STDOUT:", e.stdout, file=sys.stderr)
        print("STDERR:", e.stderr, file=sys.stderr)
        sys.exit(1)

    # The Pi script prints exactly one JSON object to stdout
    try:
        idx = completed.stdout.find("{")
        trimmed = completed.stdout[idx:].strip()

        measurement = json.loads(trimmed)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON from Pi: |{completed.stdout}|", file=sys.stderr)
        sys.exit(1)

    return measurement


def append_to_sheet(timestamp: str, values: [float]) -> None:
    """
    Use gspread + service-account to open the sheet and append a row.
    """
    gc = gspread.service_account(filename=GOOGLE_CREDENTIALS)
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.worksheet(WORKSHEET_NAME)

    # Append [timestamp, voltage]
    worksheet.append_row([timestamp] + values)


def main():
    # 1. SSH → Pi → get measurement payload
    payload = get_measurement_via_ssh()
    ts = payload.get("timestamp")
    volt = payload.get("voltage")
    amp = payload.get("current")

    power = volt * amp

    if ts is None or volt is None:
        print("ERROR: Invalid payload from Pi:", payload, file=sys.stderr)
        sys.exit(1)

    # 2. Upload to Google Sheets

    print("Appending to sheet!")

    append_to_sheet(ts, [volt, amp, power])


if __name__ == "__main__":
    main()
