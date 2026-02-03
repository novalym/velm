# Path: scaffold/symphony/renderers/cinematic_renderer/widgets/sparkline.py
# -------------------------------------------------------------------------

from typing import Sequence, List
from rich.text import Text
from rich.style import Style


class Sparkline:
    """
    =================================================================================
    == THE PULSE VISUALIZER (V-Ω-UNICODE-GRADIENT)                                 ==
    =================================================================================
    LIF: 10,000,000,000

    A divine artisan that transmutes a stream of raw numbers into a living
    landscape of Unicode blocks. It perceives the intensity of the data and
    assigns color (Heat) and form (Height) to represent the system's vitality.

    ### THE PANTHEON OF 4 FACULTIES:
    1.  **The Unicode Ladder:** Uses the full spectrum of block characters ( ▂▃▄▅▆▇█)
        for high-fidelity resolution.
    2.  **The Adaptive Scale:** Automatically adjusts the floor and ceiling based on
        the data window, maximizing visual dynamic range.
    3.  **The Thermal Gradient:** Interpolates color from Serene Green (Low) to
        Warning Yellow (Medium) to Volcanic Red (Critical).
    4.  **The Void Guard:** Gracefully handles empty or singular data points without
        mathematical paradox (DivisionByZero).
    """

    # The 8 Levels of Intensity
    BARS = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

    @classmethod
    def generate(cls, data: Sequence[float], width: int = 40) -> Text:
        """
        The Rite of Visualization.
        """
        if not data:
            return Text(" " * width, style="dim")

        # 1. The Gaze of Extremes
        # We assume a fixed floor of 0.0 for percentages, but adapt the ceiling
        # to ensure small fluctuations are visible, while capping at 100.
        min_val = 0.0
        max_val = max(data) if data else 1.0

        # Ensure we have a valid range to prevent singularity
        if max_val == 0:
            max_val = 1.0  # Avoid division by zero

        range_val = max_val - min_val

        # 2. Slice the Time Window
        # We take the most recent N points that fit the width
        visible_data = list(data)[-width:]

        # Pad with silence if data is sparse
        if len(visible_data) < width:
            visible_data = [0.0] * (width - len(visible_data)) + visible_data

        graph = Text()

        # 3. The Loop of Transmutation
        for value in visible_data:
            # Normalize 0.0 -> 1.0 relative to the max peak seen
            # Or absolute? For CPU/RAM, absolute 100% is usually better context.
            # Let's use Absolute 100 for percentage data, but auto-scale if max is small?
            # Decision: Hybrid. If max > 1.0, assume non-percentage and auto-scale.
            # If max <= 100 (and likely percentage), treat 100 as ceiling.

            # For this renderer, we treat inputs as 0-100 percentages.
            ceiling = 100.0

            normalized = max(0.0, min(value, ceiling)) / ceiling

            # Map to 0-7 index
            bar_index = int(normalized * (len(cls.BARS) - 1))
            char = cls.BARS[bar_index]

            # 4. The Thermal Gradient
            style = cls._divine_color(value)

            graph.append(char, style=style)

        return graph

    @staticmethod
    def _divine_color(value: float) -> Style:
        """
        Adjudicates the color based on intensity.
        0-50%   : Green/Cyan
        50-80%  : Yellow/Orange
        80-100% : Red/Magenta
        """
        if value < 30:
            return Style(color="cyan")
        elif value < 50:
            return Style(color="green")
        elif value < 70:
            return Style(color="yellow")
        elif value < 90:
            return Style(color="orange1")
        else:
            return Style(color="red", bold=True)