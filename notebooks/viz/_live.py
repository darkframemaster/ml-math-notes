"""Browser-side plots. Sliders update the figure without a kernel round-trip."""

from __future__ import annotations

from pathlib import Path

import anywidget
import traitlets


class LiveView(anywidget.AnyWidget):
    _esm = Path(__file__).with_name("live.js")
    spec = traitlets.Dict().tag(sync=True)


def live_view(kind: str, payload: dict, controls: list[dict]) -> LiveView:
    return LiveView(spec={"kind": kind, "payload": payload, "controls": controls})
