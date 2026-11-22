import calc

def approx(a, b, tol): assert abs(a - b) <= tol, (a, b)

# 5'10" 180 lb 28 yo male, moderate, build muscle
r = calc.calculate("male", 28, 180, "lb", 70, "in", "build_muscle", "moderate")
# BMR check by hand: kg=81.65, cm=177.8 -> 816.5+1111.25-140+5 = 1792.8 ; x1.55 = 2778.8 ; x1.1 = 3056.7
approx(r["resting_calories"], 1795, 5); approx(r["maintenance_calories"], 2780, 5); approx(r["calories"], 3055, 5)
assert r["protein_g"] == 180
kcal = r["protein_g"]*4 + r["carbs_g"]*4 + r["fat_g"]*9
approx(kcal, r["calories"], 15)

# lean-mass protein
r2 = calc.calculate("male", 28, 180, "lb", 70, "in", "build_muscle", "moderate", body_fat_percent=15)
assert r2["protein_g"] == 153, r2["protein_g"]
assert r2["protein_range_g"] == [131, 180], r2["protein_range_g"]

# metric + female fat loss, floor
r3 = calc.calculate("female", 45, 50, "kg", 155, "cm", "lose_fat", "sedentary")
assert r3["calories"] >= 1200 and r3["calorie_floor_applied"]

# fat loss raises protein, stays inside its range
r4 = calc.calculate("male", 28, 180, "lb", 70, "in", "lose_fat", "moderate")
assert r4["protein_g"] == 198 and r4["protein_range_g"] == [163, 212], (r4["protein_g"], r4["protein_range_g"])
# high body fat: target clamps up to the low end of the range, never below it
r5 = calc.calculate("male", 40, 300, "lb", 70, "in", "build_muscle", "light", body_fat_percent=40)
assert r5["protein_g"] == r5["protein_range_g"][0], r5
# carbs never negative on tiny calorie budgets
r6 = calc.calculate("female", 30, 120, "lb", 60, "in", "lose_fat", "sedentary")
assert r6["carbs_g"] >= 0 and r6["fat_g"] >= 0
# errors
for bad in [dict(age=17), dict(weight=10), dict(height=300)]:
    args = dict(sex="male", age=28, weight=180, weight_unit="lb", height=70, height_unit="in", goal="maintain", activity="light")
    args.update(bad)
    try: calc.calculate(**args); raise SystemExit("should have failed "+str(bad))
    except calc.InputError: pass
print("calc tests passed", r["calories"], r["protein_g"], r["carbs_g"], r["fat_g"])
