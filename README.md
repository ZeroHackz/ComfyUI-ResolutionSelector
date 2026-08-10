# ResolutionSelector Zerohackz

A lightweight ComfyUI custom node that outputs width, height, and frame count for MiniMax H3, driven by three simple widgets.

## Why

Swapping resolution or duration in a MiniMax H3 workflow means editing three widget values in `MiniMaxH3ImageToVideo` — width, height, and length — and remembering the 17k+5 frame-count grid rule yourself. This node centralises those choices into a single widget panel and handles the mapping for you.

## What it does

| Widget | Options | Effect |
|---|---|---|
| `orientation` | landscape / portrait | Swaps width ↔ height when portrait |
| `quality` | 360P / 480P / 720P | Maps to 736×416 / 864×480 / 1344×768 |
| `duration` | 2–10 seconds (default 5) | duration × 24 fps → snapped to MiniMax H3's 17k+5 grid |

Outputs (all `INT`):

- `width`
- `height`
- `length` (frame count)

Wire them directly into `MiniMaxH3ImageToVideo` (convert the node's widget inputs to node inputs first, or use a compatible custom node).

## Resolution table

| Quality | Pixels | Megapixels | Aspect |
|---|---|---|---|
| 360P | 736 × 416 | 0.3 | 16:9 |
| 480P | 864 × 480 | 0.4 | 16:9 |
| 720P | 1344 × 768 | 1.0 | 16:9 |

All are multiples of 32, sized for MiniMax H3's canvas constraint (`width % 32 == 0`, `height % 32 == 0`).

## Install

```powershell
cd E:\ComfyUI\custom_nodes
git clone https://github.com/Zerohackz/ResolutionSelector_Zerohackz
```

Or via ComfyUI-Manager (once listed). Restart ComfyUI. The node appears under the `ResolutionSelector_Zerohackz` category.

## Dependencies

None. Pure Python, only `comfy` imports (which every ComfyUI environment provides).

## License

MIT
