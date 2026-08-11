# MiniMax H3 Resolution Selector (ZeroHackz)

A lightweight ComfyUI custom node that outputs width, height, and frame count for MiniMax H3, driven by three simple widgets.

## Why

Swapping resolution or duration in a MiniMax H3 workflow means editing three widget values in `MiniMaxH3ImageToVideo` — width, height, and length — and remembering the 17k+5 frame-count grid rule yourself. This node centralises those choices into a single widget panel and handles the mapping for you.

## What it does

| Widget | Options | Effect |
|---|---|---|---|
| `orientation` | landscape / portrait | Swaps width ↔ height when portrait |
| `megapixels` | 0.2 MP → 2.0 MP (14 tiers) | Maps to 16:9 resolution (multiple of 32) |
| `duration` | 2–10 seconds (default 5) | duration × 24 fps → snapped to MiniMax H3's 17k+5 grid |

Outputs (all `INT`):

- `width`
- `height`
- `length` (frame count)

Wire them directly into `MiniMaxH3ImageToVideo` (convert the node's widget inputs to node inputs first, or use a compatible custom node).

## Resolution table

| Megapixels | Resolution | Aspect |
|---|---|---|
| 0.2 | 608 × 352 | 16:9 |
| 0.3 | 736 × 416 | 16:9 |
| 0.4 | 864 × 480 | 16:9 |
| 0.5 | 960 × 544 | 16:9 |
| 0.6 | 1056 × 608 | 16:9 |
| 0.7 | 1152 × 640 | 16:9 |
| 0.8 | 1216 × 672 | 16:9 |
| 0.9 | 1280 × 736 | 16:9 |
| 0.98 | 1344 × 768 | 16:9 |
| 1.0 | 1376 × 768 | 16:9 |
| 1.2 | 1504 × 832 | 16:9 |
| 1.5 | 1664 × 928 | 16:9 |
| 1.8 | 1824 × 1024 | 16:9 |
| 2.0 | 1920 × 1088 | 16:9 |

All are multiples of 32, sized for MiniMax H3's canvas constraint (`width % 32 == 0`, `height % 32 == 0`).

## Install

```powershell
cd E:\ComfyUI\custom_nodes
git clone https://github.com/Zerohackz/ComfyUI-ResolutionSelector
```

Or via ComfyUI-Manager (once listed). Restart ComfyUI. The node appears under the `MiniMax H3/ZeroHackz` category.

## Dependencies

None. Pure Python, only `comfy` imports (which every ComfyUI environment provides).

## License

MIT
