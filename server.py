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

mcp = MCPServer(
    "AM Training Co Macro Calculator",
    title="AM Training Co Macro Calculator",
    description="Free daily calorie and macro estimates for building muscle, losing fat or maintaining weight.",
    website_url="https://forms.gle/8LbdUhkZcYXRcBNu9",
    icons=[ICON],
)


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
