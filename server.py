"""AM Training Co Macro Calculator: MCP server for ChatGPT (Apps SDK). Stores nothing."""
import os
from typing import Literal, Optional

from mcp.server.mcpserver import MCPServer
from mcp_types import Icon, ToolAnnotations

import calc

ICON = Icon(
    src="https://raw.githubusercontent.com/AMTrainingCo/am-macro-calculator/main/icon.png",
    mime_type="image/png",
    sizes=["512x512"],
)

WIDGET_URI = "ui://widget/am-macro-calculator.html"

WIDGET_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>AM Training Co Macro Calculator</title>
<style>
  :root {
    --navy: #14183a;
    --navy-2: #1d2250;
    --line: #343a73;
    --pink: #ed3cb3;
    --cyan: #1cb1d5;
    --text: #ffffff;
    --muted: #aab0d6;
    --error: #ff8a9b;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    background: var(--navy);
    color: var(--text);
    padding: 16px;
    line-height: 1.4;
  }
  .wrap { max-width: 560px; margin: 0 auto; }
  header { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
  .logo {
    width: 44px; height: 44px; border-radius: 12px; background: var(--navy-2);
    border: 3px solid transparent;
    background-image: linear-gradient(var(--navy), var(--navy)), conic-gradient(var(--pink) 0 40%, var(--cyan) 40% 75%, #fff 75% 100%);
    background-origin: border-box; background-clip: padding-box, border-box;
    display: grid; place-items: center; font-weight: 800; font-size: 15px;
  }
  h1 { font-size: 18px; margin: 0; }
  h1 span { color: var(--pink); }
  .sub { color: var(--muted); font-size: 12.5px; margin: 2px 0 0; }
  .card { background: var(--navy-2); border: 1px solid var(--line); border-radius: 16px; padding: 16px; }
  .row { display: grid; gap: 10px; margin-bottom: 12px; }
  .row.two { grid-template-columns: 1fr 1fr; }
  .row.three { grid-template-columns: 1fr 1fr 1fr; }
  label { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; font-weight: 600; letter-spacing: .02em; }
  input, select {
    width: 100%; background: var(--navy); color: var(--text); border: 1px solid var(--line);
    border-radius: 10px; padding: 10px 11px; font-size: 15px; outline: none;
  }
  input:focus, select:focus { border-color: var(--cyan); box-shadow: 0 0 0 2px rgba(28,177,213,.25); }
  .seg { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
  .seg button {
    background: var(--navy); color: var(--muted); border: 0; padding: 10px; font-size: 14px; font-weight: 600; cursor: pointer;
  }
  .seg button.on { background: var(--cyan); color: #04131a; }
  .hint { font-size: 11.5px; color: var(--muted); margin-top: 4px; }
  .go {
    width: 100%; margin-top: 4px; padding: 13px; border: 0; border-radius: 12px; cursor: pointer;
    background: var(--pink); color: #fff; font-size: 16px; font-weight: 800; letter-spacing: .02em;
  }
  .go:disabled { opacity: .6; cursor: default; }
  .err { color: var(--error); font-size: 13px; margin: 10px 0 0; min-height: 0; }
  #result { display: none; margin-top: 14px; }
  .kcal-label { font-size: 12px; color: var(--muted); font-weight: 700; letter-spacing: .06em; }
  .kcal { font-size: 40px; font-weight: 800; color: #3ddc97; line-height: 1.1; margin: 2px 0; }
  .note { font-size: 12.5px; color: var(--muted); }
  .macros { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 14px 0 10px; }
  .m { background: var(--navy); border: 1px solid var(--line); border-radius: 12px; padding: 10px; }
  .m b { display: block; font-size: 22px; }
  .m span { font-size: 12px; color: var(--muted); }
  .m.p b { color: var(--pink); }
  .m.c b { color: var(--cyan); }
  .m.f b { color: #ffd166; }
  .bar { display: flex; height: 10px; border-radius: 99px; overflow: hidden; margin: 6px 0 4px; }
  .bar i { display: block; height: 100%; }
  .box { background: var(--navy); border: 1px solid var(--line); border-radius: 12px; padding: 11px 12px; margin-top: 10px; font-size: 13.5px; }
  .box h3 { margin: 0 0 4px; font-size: 13px; color: var(--cyan); letter-spacing: .04em; }
  .disc { font-size: 11.5px; color: var(--muted); margin-top: 12px; }
  .cta { margin-top: 14px; padding: 14px; border-radius: 14px; background: linear-gradient(135deg, rgba(237,60,179,.18), rgba(28,177,213,.18)); border: 1px solid var(--line); }
  .cta p { margin: 0 0 10px; font-size: 14px; }
  .cta button {
    width: 100%; padding: 12px; border: 0; border-radius: 11px; cursor: pointer;
    background: var(--cyan); color: #04131a; font-size: 15px; font-weight: 800;
  }
  .cta .url { margin-top: 8px; font-size: 12px; color: var(--muted); word-break: break-all; }
  .cta .ig { margin-top: 6px; font-size: 13px; color: var(--muted); }
  .cta .ig b { color: var(--text); }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="logo">AM</div>
    <div>
      <h1>Macro <span>Calculator</span></h1>
      <p class="sub">Free daily calorie and macro estimate. Nothing is saved.</p>
    </div>
  </header>

  <div class="card">
    <div class="row two">
      <div>
        <label>SEX</label>
        <div class="seg" id="sex">
          <button type="button" data-v="male" class="on">Male</button>
          <button type="button" data-v="female">Female</button>
        </div>
      </div>
      <div>
        <label>UNITS</label>
        <div class="seg" id="units">
          <button type="button" data-v="imperial" class="on">lb / ft</button>
          <button type="button" data-v="metric">kg / cm</button>
        </div>
      </div>
    </div>

    <div class="row three">
      <div>
        <label for="age">AGE</label>
        <input id="age" type="number" inputmode="numeric" min="18" max="90" placeholder="28" />
      </div>
      <div>
        <label for="weight" id="weightLabel">WEIGHT (LB)</label>
        <input id="weight" type="number" inputmode="decimal" placeholder="180" />
      </div>
      <div id="heightImperial">
        <label>HEIGHT (FT / IN)</label>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">
          <input id="ft" type="number" inputmode="numeric" min="3" max="8" placeholder="5" aria-label="feet" />
          <input id="inch" type="number" inputmode="numeric" min="0" max="11" placeholder="10" aria-label="inches" />
        </div>
      </div>
      <div id="heightMetric" style="display:none">
        <label for="cm">HEIGHT (CM)</label>
        <input id="cm" type="number" inputmode="decimal" placeholder="178" />
      </div>
    </div>

    <div class="row two">
      <div>
        <label for="goal">GOAL</label>
        <select id="goal">
          <option value="build_muscle">Build muscle</option>
          <option value="lose_fat">Lose fat</option>
          <option value="maintain">Maintain weight</option>
        </select>
      </div>
      <div>
        <label for="activity">ACTIVITY LEVEL</label>
        <select id="activity">
          <option value="sedentary">Sedentary (desk job, little exercise)</option>
          <option value="light">Light (1 to 3 workouts a week)</option>
          <option value="moderate" selected>Moderate (3 to 5 workouts a week)</option>
          <option value="heavy">Heavy (6 to 7 hard workouts a week)</option>
        </select>
      </div>
    </div>

    <div class="row" style="margin-bottom:6px">
      <div>
        <label for="bf">BODY FAT % (OPTIONAL)</label>
        <input id="bf" type="number" inputmode="decimal" min="3" max="60" placeholder="Leave blank if you don't know" />
        <div class="hint">If you add it, protein is based on your lean mass.</div>
      </div>
    </div>

    <button class="go" id="go" type="button">Calculate my macros</button>
    <div class="err" id="err" role="alert"></div>
  </div>

  <div id="result" class="card">
    <div class="kcal-label">DAILY CALORIE TARGET</div>
    <div class="kcal"><span id="kcal">0</span> kcal</div>
    <div class="note" id="kcalNote"></div>

    <div class="macros">
      <div class="m p"><b id="pg">0g</b><span>Protein</span><br /><span id="pc"></span></div>
      <div class="m c"><b id="cg">0g</b><span>Carbs</span><br /><span id="cc"></span></div>
      <div class="m f"><b id="fg">0g</b><span>Fat</span><br /><span id="fc"></span></div>
    </div>
    <div class="bar"><i id="bp" style="background:var(--pink)"></i><i id="bc" style="background:var(--cyan)"></i><i id="bf2" style="background:#ffd166"></i></div>

    <div class="box"><h3>PROTEIN RANGE</h3><span id="prange"></span></div>
    <div class="box"><h3>HOW TO USE THESE NUMBERS</h3><span id="how"></span></div>
    <div class="disc" id="disc"></div>

    <div class="cta">
      <p>These are starting numbers. Want a plan built around your body, schedule and gym?</p>
      <button type="button" id="apply">Apply at AM Training Co</button>
      <div class="url">https://forms.gle/8LbdUhkZcYXRcBNu9</div>
      <div class="ig">Or follow <b>@aaron_munoz1</b> on Instagram.</div>
    </div>
  </div>
</div>

<script type="module">
  const FORM_URL = "https://forms.gle/8LbdUhkZcYXRcBNu9";
  const $ = (id) => document.getElementById(id);

  // ---------- MCP Apps bridge (JSON-RPC over postMessage) ----------
  const pending = new Map();
  let seq = 0;
  const post = (m) => window.parent.postMessage({ jsonrpc: "2.0", ...m }, "*");
  const rpc = (method, params) =>
    new Promise((resolve, reject) => {
      const id = ++seq;
      pending.set(id, { resolve, reject });
      post({ id, method, params });
      setTimeout(() => {
        if (pending.has(id)) { pending.delete(id); reject(new Error("Timed out")); }
      }, 20000);
    });
  window.addEventListener("message", (e) => {
    if (e.source !== window.parent) return;
    const m = e.data;
    if (!m || m.jsonrpc !== "2.0") return;
    if (typeof m.id === "number" && pending.has(m.id)) {
      const p = pending.get(m.id);
      pending.delete(m.id);
      m.error ? p.reject(m.error) : p.resolve(m.result);
    }
  });
  const ready = (async () => {
    try {
      await rpc("ui/initialize", {
        appInfo: { name: "am-macro-calculator", version: "1.0.0" },
        appCapabilities: {},
        protocolVersion: "2026-01-26",
      });
      post({ method: "ui/notifications/initialized", params: {} });
      return true;
    } catch (e) { return false; }
  })();

  async function callTool(name, args) {
    if (window.openai && typeof window.openai.callTool === "function") {
      try { return await window.openai.callTool(name, args); } catch (e) { /* fall back to the bridge */ }
    }
    await ready;
    return await rpc("tools/call", { name, arguments: args });
  }

  async function openLink(url) {
    try {
      if (window.openai && typeof window.openai.openExternal === "function") {
        window.openai.openExternal({ href: url });
        return;
      }
    } catch (e) {}
    try { await rpc("ui/open-link", { url }); return; } catch (e) {}
    window.open(url, "_blank", "noopener");
  }

  function parseResult(r) {
    if (!r) return null;
    if (r.structuredContent && (r.structuredContent.calories !== undefined || r.structuredContent.error)) return r.structuredContent;
    const t = (r.content || []).find((c) => c && c.type === "text");
    if (t) { try { return JSON.parse(t.text); } catch (e) {} }
    if (typeof r.result === "string") { try { return JSON.parse(r.result); } catch (e) {} }
    if (r.result && typeof r.result === "object") return parseResult(r.result);
    if (r.calories !== undefined || r.error) return r;
    return null;
  }

  // ---------- Form ----------
  let sex = "male";
  let units = "imperial";
  const seg = (id, cb) => {
    $(id).addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      [...$(id).children].forEach((x) => x.classList.toggle("on", x === b));
      cb(b.dataset.v);
    });
  };
  seg("sex", (v) => { sex = v; });
  seg("units", (v) => {
    units = v;
    const imp = v === "imperial";
    $("weightLabel").textContent = imp ? "WEIGHT (LB)" : "WEIGHT (KG)";
    $("weight").placeholder = imp ? "180" : "82";
    $("heightImperial").style.display = imp ? "" : "none";
    $("heightMetric").style.display = imp ? "none" : "";
  });

  const num = (id) => { const v = $(id).value.trim(); return v === "" ? null : Number(v); };
  const fmt = (n) => Number(n).toLocaleString("en-US");

  function showError(msg) { $("err").textContent = msg || ""; }

  $("go").addEventListener("click", async () => {
    showError("");
    const age = num("age");
    const weight = num("weight");
    let height;
    if (units === "imperial") {
      const ft = num("ft");
      const inch = num("inch") || 0;
      height = ft === null ? null : ft * 12 + inch;
    } else {
      height = num("cm");
    }
    if (age === null || weight === null || height === null) {
      showError("Please fill in age, weight and height.");
      return;
    }
    const args = {
      sex, age: Math.round(age), weight, weight_unit: units === "imperial" ? "lb" : "kg",
      height, height_unit: units === "imperial" ? "in" : "cm",
      goal: $("goal").value, activity: $("activity").value,
    };
    const bf = num("bf");
    if (bf !== null) args.body_fat_percent = bf;

    $("go").disabled = true;
    $("go").textContent = "Calculating...";
    try {
      const data = parseResult(await callTool("calculate_macros", args));
      if (!data) throw new Error("No result came back. Please try again.");
      if (data.error) { showError(data.error); return; }
      render(data);
    } catch (e) {
      showError((e && e.message) || "Something went wrong. Please try again in a moment.");
    } finally {
      $("go").disabled = false;
      $("go").textContent = "Calculate my macros";
    }
  });

  function render(d) {
    $("kcal").textContent = fmt(d.calories);
    $("kcalNote").textContent = "Estimated maintenance: " + fmt(d.maintenance_calories) + " kcal. Target is " + d.goal_note + ".";
    const pc = d.protein_g * 4, cc = d.carbs_g * 4, fc = d.fat_g * 9;
    $("pg").textContent = d.protein_g + "g"; $("pc").textContent = fmt(pc) + " calories";
    $("cg").textContent = d.carbs_g + "g";   $("cc").textContent = fmt(cc) + " calories";
    $("fg").textContent = d.fat_g + "g";     $("fc").textContent = fmt(fc) + " calories";
    const tot = pc + cc + fc || 1;
    $("bp").style.width = (pc / tot * 100) + "%";
    $("bc").style.width = (cc / tot * 100) + "%";
    $("bf2").style.width = (fc / tot * 100) + "%";
    const r = d.protein_range_g || [];
    $("prange").textContent = (r.length === 2 ? r[0] + " to " + r[1] + " g per day. " : "") + (d.protein_range_note || "") + " Your target uses " + (d.protein_basis || "") + ".";
    $("how").textContent = d.how_to_use || "";
    $("disc").textContent = "Disclaimer: " + (d.disclaimer || "");
    if (d.calorie_floor_applied) {
      $("kcalNote").textContent += " A minimum calorie floor was applied for safety.";
    }
    $("result").style.display = "block";
    $("result").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  $("apply").addEventListener("click", () => openLink(FORM_URL));
</script>
</body>
</html>
"""

mcp = MCPServer(
    "AM Training Co Macro Calculator",
    title="AM Training Co Macro Calculator",
    description="Free daily calorie and macro estimates for building muscle, losing fat or maintaining weight.",
    website_url="https://forms.gle/8LbdUhkZcYXRcBNu9",
    icons=[ICON],
)


@mcp.resource(
    WIDGET_URI,
    name="am-macro-calculator-widget",
    title="AM Training Co Macro Calculator screen",
    description="Calculator screen with fields, a Calculate button and the results.",
    mime_type="text/html;profile=mcp-app",
    meta={"ui": {"prefersBorder": True}},
)
def calculator_widget() -> str:
    return WIDGET_HTML


@mcp.tool(
    name="open_macro_calculator",
    title="Open macro calculator",
    description=(
        "Use this when someone wants to open or use the AM Training Co macro calculator, or asks for a calculator "
        "screen, a form, or says they want to calculate macros without giving all their details yet. "
        "It shows a calculator screen with fields for sex, age, weight, height, goal and activity level. "
        "If the person already gave all of those details in their message, call calculate_macros instead."
    ),
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False, idempotentHint=True),
    meta={
        "ui": {"resourceUri": WIDGET_URI},
        "openai/outputTemplate": WIDGET_URI,
        "openai/toolInvocation/invoking": "Opening the calculator...",
        "openai/toolInvocation/invoked": "Calculator ready.",
    },
)
def open_macro_calculator() -> dict:
    """Show the macro calculator screen."""
    return {
        "assistant_instructions": (
            "The calculator screen is now showing. Reply with one short sentence telling the person to fill it in "
            "and press Calculate my macros. Do not list the fields, do not calculate anything yourself, "
            "and do not repeat the form in text."
        ),
        "status": "calculator_shown",
    }


@mcp.tool(
    name="calculate_macros",
    description=(
        "Use this when someone wants a daily calorie target and protein, carb and fat grams "
        "for building muscle, losing fat or maintaining weight. Needs sex, age (18+), weight, height, "
        "goal and activity level. Body fat percent is optional. Returns estimates only, nothing is stored."
    ),
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False, idempotentHint=True),
)
def calculate_macros(
    sex: Literal["male", "female"],
    age: int,
    weight: float,
    weight_unit: Literal["lb", "kg"],
    height: float,
    height_unit: Literal["in", "cm"],
    goal: Literal["build_muscle", "lose_fat", "maintain"],
    activity: Literal["sedentary", "light", "moderate", "heavy"],
    body_fat_percent: Optional[float] = None,
) -> dict:
    """Return daily calories and macros. height_unit 'in' means total inches (5 ft 10 in = 70)."""
    try:
        return calc.calculate(sex, age, weight, weight_unit, height, height_unit, goal, activity, body_fat_percent)
    except calc.InputError as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8000")),
        stateless_http=True,
        json_response=True,
    )
