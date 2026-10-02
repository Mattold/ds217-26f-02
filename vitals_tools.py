"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return a list of the systolic blood pressure readings from encounter records."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """Return the average, or None if there are no readings."""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Returns distinct patient IDs from a list of encounter records."""
    patient_ids = set()
    for encounter in encounters:
        patient_ids.add(encounter["patient_id"])
    return len(patient_ids)

def patients_at_or_above(encounters, cutoff):
    """Returns a list of patient IDs whose systolic reading is at or above the cutoff."""
    patient_ids = []
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            patient_ids.append(encounter["patient_id"])
    return patient_ids