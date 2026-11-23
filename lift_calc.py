"""Lift math for the AM Training Co calculators: estimated 1RM, percentage table, plate math.

Pure functions, no storage. Estimates only.
"""
from typing import Optional

LB_PLATES = [45, 35, 25, 10, 5, 2.5]
KG_PLATES = [25, 20, 15, 10, 5, 2.5, 1.25]

# (percent of 1RM, rough use). Guide only: real rep strength varies by person and lift.
PERCENT_ROWS = [
    (95, "Heavy single or double"),
    (90, "Heavy double or triple"),
    (85, "3 to 5 reps (strength)"),
    (80, "5 to 6 reps"),
    (75, "6 to 8 reps (size)"),
    (70, "8 to 10 reps (size)"),
    (65, "10 to 12 reps"),
    (60, "12 to 15 reps (endurance)"),
    (50, "Warm-up or light technique work"),
]

DISCLAIMER = (
    "These are estimates, not medical advice. Warm up first, use a spotter or safeties for heavy sets, "
    "and do not test a true one-rep max alone. If something hurts, stop and talk to a doctor or coach."
)
NEXT_STEP = (
    "Want a full program built around your lifts, schedule and gym? Apply at AM Training Co: "
    "https://forms.gle/8LbdUhkZcYXRcBNu9 or follow @aaron_munoz1 on Instagram and AM Training Co on Facebook."
)


class InputError(ValueError):
    pass


def _clean(n: float) -> float:
    """Drop a trailing .0 so 225.0 shows as 225."""
    return int(n) if float(n).is_integer() else n


def _check_unit(unit: str) -> str:
    if unit not in ("lb", "kg"):
        raise InputError("Unit must be lb or kg.")
    return unit


def default_bar(unit: str) -> float:
    return 45 if unit == "lb" else 20


def smallest_jump(unit: str) -> float:
    """Smallest total change you can make to the bar: one smallest plate on each side."""
    return 2 * (LB_PLATES[-1] if unit == "lb" else KG_PLATES[-1])


def estimate_1rm(weight: float, reps: int) -> float:
    """Average of the Epley and Brzycki formulas. One rep is the weight itself."""
    if reps == 1:
        return float(weight)
    epley = weight * (1 + reps / 30)
    brzycki = weight * 36 / (37 - reps)
    return (epley + brzycki) / 2


def _round_total(x: float, unit: str) -> float:
    return round(x) if unit == "lb" else round(x * 2) / 2


def plates_for(total: float, unit: str, bar: Optional[float] = None) -> dict:
    """Plates per side to load `total` on a bar. Rounds to the nearest weight that can be loaded."""
    _check_unit(unit)
    bar = default_bar(unit) if bar is None else bar
    if bar < 0:
        raise InputError("Bar weight cannot be negative.")
    if total < bar:
        return {"loaded": _clean(total), "bar": _clean(bar), "plates": [], "text": "Under the bar weight", "under_bar": True}
    plates = LB_PLATES if unit == "lb" else KG_PLATES
    step = plates[-1]
    per_side = (total - bar) / 2
    per_side = round(per_side / step + 1e-9) * step  # nearest loadable (half-up)
    loaded = bar + 2 * per_side
    left = per_side
    used = []
    for p in plates:
        c = int((left + 1e-9) // p)
        if c:
            used.append({"plate": _clean(p), "count": c})
            left -= c * p
    if not used:
        text = "Bar only"
    else:
        text = " + ".join((f"{u['count']}x{u['plate']}" if u["count"] > 1 else f"{u['plate']}") for u in used)
        text += " per side"
    return {"loaded": _clean(round(loaded, 2)), "bar": _clean(bar), "plates": used, "text": text, "under_bar": False}


def calculate(weight: float, weight_unit: str, reps: int, lift: Optional[str] = None, bar_weight: Optional[float] = None) -> dict:
    _check_unit(weight_unit)
    if not isinstance(reps, int) or reps < 1 or reps > 12:
        raise InputError("Reps must be a whole number from 1 to 12. For sets above 12 the estimate is too rough.")
    if weight is None or weight <= 0 or weight > (2000 if weight_unit == "lb" else 900):
        raise InputError("Enter the weight you lifted as a positive number.")
    bar = default_bar(weight_unit) if bar_weight is None else bar_weight
    if bar < 0 or bar > (150 if weight_unit == "lb" else 70):
        raise InputError("Bar weight looks off. A standard bar is 45 lb or 20 kg.")

    one_rm = estimate_1rm(weight, reps)
    one_rm_r = _round_total(one_rm, weight_unit)

    rows = []
    for pct, use in PERCENT_ROWS:
        raw = one_rm * pct / 100
        p = plates_for(raw, weight_unit, bar)
        rows.append({
            "percent": pct,
            "weight": p["loaded"] if not p["under_bar"] else _clean(_round_total(raw, weight_unit)),
            "plates": p["text"],
            "use": use,
        })

    if reps <= 5:
        accuracy = "High. Sets of 1 to 5 reps give the best estimate."
    elif reps <= 8:
        accuracy = "Good. A heavier set of 3 to 5 reps would tighten the number."
    else:
        accuracy = "Rough. Sets of 9 to 12 reps are less accurate, so treat this as a ballpark."

    label = (lift or "").strip()[:40]
    return {
        "lift": label or None,
        "unit": weight_unit,
        "entered": f"{_clean(weight)} {weight_unit} x {reps}",
        "estimated_1rm": _clean(one_rm_r),
        "accuracy": accuracy,
        "bar_weight": _clean(bar),
        "table": rows,
        "table_note": "Weights are rounded to what you can load with standard plates. The rep guide is rough, so use how the set feels to adjust.",
        "disclaimer": DISCLAIMER,
        "next_step": NEXT_STEP,
    }


def plate_math(target: float, unit: str, bar_weight: Optional[float] = None) -> dict:
    _check_unit(unit)
    if target is None or target <= 0 or target > (2000 if unit == "lb" else 900):
        raise InputError("Enter the total weight you want on the bar.")
    bar = default_bar(unit) if bar_weight is None else bar_weight
    if bar < 0 or bar > (150 if unit == "lb" else 70):
        raise InputError("Bar weight looks off. A standard bar is 45 lb or 20 kg.")
    p = plates_for(target, unit, bar)
    out = {"unit": unit, "requested": _clean(target), "bar_weight": p["bar"], "loaded_total": p["loaded"],
           "plates_per_side": p["plates"], "text": p["text"]}
    if p["under_bar"]:
        out["note"] = "That is lighter than the bar. Use a lighter bar or dumbbells."
    elif abs(p["loaded"] - target) > 1e-6:
        out["note"] = f"Closest weight you can load is {p['loaded']} {unit}. The smallest jump is {_clean(smallest_jump(unit))} {unit}."
    return out
