# AM Training Co Macro Calculator (ChatGPT app / MCP server)

Takes sex, age (18+), weight, height, goal, activity (and optional body fat %) and returns
daily calories + protein/carbs/fat. Stores nothing. Ends with your intake form link and @aaron_munoz1.

## Files
- calc.py       the math (Mifflin-St Jeor, activity factor, goal adjustment, 1 g protein per lb lean mass or body weight)
- server.py     the MCP server (one tool: calculate_macros), endpoint /mcp
- test_calc.py  checks the math:  python3 test_calc.py

## Run locally
    pip install -r requirements.txt
    PORT=8000 python3 server.py        # serves http://localhost:8000/mcp

## Before it goes public (not done yet)
1. Host it at a stable public HTTPS URL (any free-tier Python host works) with the /mcp path.
2. Test it in ChatGPT developer mode using that URL.
3. Submit through the OpenAI developer portal. Expect to need: a privacy policy page, a support contact,
   test prompts, and a branded name. Check their current submission guidelines first.

## Numbers (all adjustable in calc.py)
- Goal: build muscle +10%, lose fat -20%, maintain 0%. Calorie floor 1500 (male) / 1200 (female).
- Protein target: 1 g per lb of lean mass if body fat % given, otherwise 1 g per lb of body weight, kept inside 1.6-2.2 g/kg of body weight.
  Fat loss: 1.1 g per lb target inside 2.0-2.6 g/kg. The range is returned alongside the target.
- Fat: 25% of calories. Carbs: the rest.
