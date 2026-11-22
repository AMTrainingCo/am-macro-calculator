"""AM Training Co macro calculator: pure functions, no I/O, nothing stored."""

LB_PER_KG = 2.20462
CM_PER_IN = 2.54

ACTIVITY = {
    "sedentary": (1.2, "mostly sitting, little training"),
    "light": (1.375, "light training 1-3 days a week"),
    "moderate": (1.55, "moderate training 3-5 days a week"),
    "heavy": (1.725, "hard training 6-7 days a week or a physical job"),
}
GOALS = {
    "build_muscle": (0.10, "a small surplus (+10%) to build muscle with minimal fat gain"),
    "lose_fat": (-0.20, "a moderate deficit (-20%) to lose fat while keeping muscle"),
    "maintain": (0.0, "maintenance calories"),
}
FLOOR = {"male": 1500, "female": 1200}

CTA = (
    "These are starting numbers. Want a plan built around your body, schedule and gym? "
    "Apply at AM Training Co: https://forms.gle/8LbdUhkZcYXRcBNu9 or follow @aaron_munoz1 on Instagram."
)


class InputError(ValueError):
    pass


def calculate(sex, age, weight, weight_unit, height, height_unit, goal, activity, body_fat_percent=None):
    sex = str(sex).lower().strip()
    goal = str(goal).lower().strip()
    activity = str(activity).lower().strip()
    weight_unit = str(weight_unit).lower().strip()
    height_unit = str(height_unit).lower().strip()

    if sex not in FLOOR:
        raise InputError("sex must be 'male' or 'female'")
    if goal not in GOALS:
        raise InputError("goal must be build_muscle, lose_fat or maintain")
    if activity not in ACTIVITY:
        raise InputError("activity must be sedentary, light, moderate or heavy")
    if weight_unit not in ("lb", "kg"):
        raise InputError("weight_unit must be 'lb' or 'kg'")
    if height_unit not in ("in", "cm"):
        raise InputError("height_unit must be 'in' or 'cm'")
    if age < 18:
        raise InputError("This calculator is for adults 18 and over. If you're under 18, talk with a doctor or a qualified coach.")
    if age > 90:
        raise InputError("Please enter an age between 18 and 90.")

    kg = weight / LB_PER_KG if weight_unit == "lb" else weight
    cm = height * CM_PER_IN if height_unit == "in" else height
    if not 35 <= kg <= 250:
        raise InputError("Weight looks out of range. Please double-check it.")
    if not 120 <= cm <= 230:
        raise InputError("Height looks out of range. Please double-check it.")
    if body_fat_percent is not None and not 3 <= body_fat_percent <= 60:
        raise InputError("Body fat percent should be between 3 and 60, or left blank.")

    lb = kg * LB_PER_KG
    bmr = 10 * kg + 6.25 * cm - 5 * age + (5 if sex == "male" else -161)
    maintenance = bmr * ACTIVITY[activity][0]
    target = maintenance * (1 + GOALS[goal][0])

    floored = False
    if target < FLOOR[sex]:
        target = FLOOR[sex]
        floored = True

    # Protein: target per lb of lean mass (if body fat given) else body weight, kept inside a
    # research-based range per kg of body weight. Fat loss gets a higher target and range.
    if goal == "lose_fat":
        per_lb, lo_kg, hi_kg = 1.1, 2.0, 2.6
    else:
        per_lb, lo_kg, hi_kg = 1.0, 1.6, 2.2
    if body_fat_percent is not None:
        basis_lb = lb * (1 - body_fat_percent / 100)
        protein_basis = f"{per_lb:g} g per lb of lean body mass"
    else:
        basis_lb = lb
        protein_basis = f"{per_lb:g} g per lb of body weight (add a body fat % for a lean-mass based number)"
    p_low, p_high = kg * lo_kg, kg * hi_kg
    protein = min(max(basis_lb * per_lb, p_low), p_high)

    fat = target * 0.25 / 9
    carbs = (target - protein * 4 - fat * 9) / 4
    if carbs < 0:
        carbs = 0.0
        # keep totals honest if protein alone is very high relative to calories
        fat = max(0.0, (target - protein * 4) / 9)

    return {
        "calories": round(target / 5) * 5,
        "protein_g": round(protein),
        "protein_range_g": [round(p_low), round(p_high)],
        "protein_range_note": f"Research-based range for this goal: {lo_kg:g} to {hi_kg:g} g per kg of body weight.",
        "carbs_g": round(carbs),
        "fat_g": round(fat),
        "maintenance_calories": round(maintenance / 5) * 5,
        "resting_calories": round(bmr / 5) * 5,
        "goal_note": GOALS[goal][1],
        "protein_basis": protein_basis,
        "calorie_floor_applied": floored,
        "how_to_use": (
            "Eat close to these numbers for 2 to 3 weeks and weigh yourself the same way each morning. "
            "If your weekly average isn't moving the way you want, adjust calories by about 100 to 200."
        ),
        "disclaimer": (
            "These are estimates, not medical advice. Talk with a doctor first if you have a medical condition, "
            "are pregnant or nursing, or have a history of disordered eating."
        ),
        "next_step": CTA,
    }
