# AM Training Co Calculators (ChatGPT app / MCP server)

Free calculators from AM Training Co, in one ChatGPT custom plugin. Nothing is stored. Each result ends with the coaching application form link, @aaron_munoz1 on Instagram and AM Training Co on Facebook.

## Calculators

**Macro calculator.** Takes sex, age (18+), weight, height, goal, activity level (and optional body fat %) and returns daily calories plus protein, carbs and fat.

**Lift calculator.** Estimates a one-rep max from a recent set (weight and reps), then shows working weights from 50% to 95% with the plates to load on each side of the bar. A Plate math tab shows the plates for any target weight.

## Files

- `calc.py`: macro math (Mifflin-St Jeor, activity factor, goal adjustment, 1 g protein per lb lean mass or body weight)
- `lift_calc.py`: lift math (Epley and Brzycki averaged for the 1RM, plate rounding to what can be loaded)
- `server.py`: the MCP server. Endpoint is `/mcp`. Tools: `open_macro_calculator`, `calculate_macros`, `open_lift_calculator`, `calculate_lift`, `plate_math`. Both calculator screens are built into this file.
- `test_calc.py`: checks the macro math. Run `python3 test_calc.py`
- `requirements.txt`: Python packages
- `icon.png`: plugin icon

## Run locally

```
pip install -r requirements.txt
python3 server.py
```

The server listens on `/mcp`.

## Deploy

Hosted free on Render. Pushing to `main` redeploys automatically. The free host sleeps when idle, so the first request can take up to a minute.

## Connect in ChatGPT

Do this on a computer, not a phone.

1. Open chatgpt.com and go to chatgpt.com/plugins.
2. Click +, then Add custom MCP server.
3. Name: AM Training Co Calculators
4. Server URL: https://am-macro-calculator.onrender.com/mcp
5. Authentication: No authentication. Save.
6. In a new chat, type "Open the macro calculator" or "Open the lift calculator".

These are estimates, not medical advice.
