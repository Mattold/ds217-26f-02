#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """A usable encounter has three fields, a patient ID, a date, and a systolic reading between 50 and 250.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    encounters = []
    skipped = 0
    with open(data_path) as file:
        lines = file.readlines()
        data_rows = lines[1:]  # Skip the header line
    for row in data_rows:
        fields = row.strip().split(",")
        if len(fields) != 3:
            skipped += 1
            print(f"Skipping row: {row.strip()} (incorrect number of fields)")
            continue
        try:
            systolic = int(fields[2])
        except ValueError:
                skipped += 1
                print(f"Skipping row: {row.strip()} (systolic reading is not an integer)")
                continue
        if not (50 <= systolic <= 250):
            skipped += 1
            print(f"Skipping row: {row.strip()} (systolic reading is out of plausible range)")
            continue
        encounters.append({
            "patient_id": fields[0],
            "date": fields[1],
            "systolic": systolic
        })
    return encounters, skipped


def main():
    """Creates a summary of the clinic encounters vitals and a follow-up list of patients with high readings."""
    encounters, skipped = read_encounters(DATA_PATH)
    readings = systolic_readings(encounters)
    usable_count = len(encounters)
    patient_count = count_patients(encounters)
    mean_reading = mean_systolic(readings)
    max_reading = max(readings) if readings else None
    min_reading = min(readings) if readings else None

    vitals_report_path = OUTPUT_DIR / "vitals_report.txt"
    report_lines = [
        f"Usable encounters: {usable_count}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {patient_count}",
        f"Mean systolic: {mean_reading:.1f} mmHg",
        f"Highest systolic: {max_reading} mmHg",
        f"Lowest systolic: {min_reading} mmHg"
    ]
    report_content = "\n".join(report_lines) + "\n"

    with open(vitals_report_path, "w") as f:
        f.write(report_content)

    print("\n--- Saved vitals_report.txt ---")
    with open(vitals_report_path, "r") as f:
        print(f.read())

    cutoff = 140
    reason = "Systolic Readings at or above 140 mmHg are considered stage 2 hypertension and require follow-up."
    followup_patients = patients_at_or_above(encounters, cutoff)
    unique_followup_patients = list(dict.fromkeys(followup_patients)) 

    followup_path = OUTPUT_DIR / "followup_list.txt"
    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
    ] + unique_followup_patients
    followup_content = "\n".join(followup_lines) + "\n"

    with open(followup_path, "w") as f:
        f.write(followup_content)

    print("\n--- Saved followup_list.txt ---")
    with open(followup_path, "r") as f:
        print(f.read())

if __name__ == "__main__":
    main()
