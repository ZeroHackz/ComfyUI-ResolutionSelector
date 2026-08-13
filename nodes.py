"""
ResolutionSelector_Zerohackz

Nodes for MiniMax H3 resolution and duration selection.
"""

import math
import logging

import torch

RESOLUTIONS = {
    "0.2 (608x352)":   (608, 352),
    "0.3 (736x416)":   (736, 416),
    "0.4 (864x480)":   (864, 480),
    "0.5 (960x544)":   (960, 544),
    "0.6 (1056x608)":  (1056, 608),
    "0.7 (1152x640)":  (1152, 640),
    "0.8 (1216x672)":  (1216, 672),
    "0.9 (1280x736)":  (1280, 736),
    "0.98 (1344x768)": (1344, 768),
    "1.0 (1376x768)":  (1376, 768),
    "1.2 (1504x832)":  (1504, 832),
    "1.5 (1664x928)":  (1664, 928),
    "1.8 (1824x1024)": (1824, 1024),
    "2.0 (1920x1088)": (1920, 1088),
}

FPS = 24

LOG = logging.getLogger("ResolutionSelector")


def snap_frames(n):
    """Snap a frame count up to MiniMax H3's 17k+5 grid."""
    while n % 17 != 5:
        n += 1
    return n


def _exact_ratio_scales(w, h, max_mp=2.0):
    """Return all valid (k, width, height) scales at the exact W:H ratio.

    Both output dimensions are guaranteed divisible by 32 for every entry,
    and every entry stays at or below max_mp megapixels. k_current is the k
    value of the original size (only present in the list if it fits).
    """
    w = max(32, (w // 32) * 32)
    h = max(32, (h // 32) * 32)
    g = math.gcd(w // 32, h // 32)
    u_w = (w // 32) // g
    u_h = (h // 32) // g
    k_current = g
    scales = []
    k = 1
    while True:
        out_w = u_w * k * 32
        out_h = u_h * k * 32
        if (out_w * out_h) / 1_000_000 > max_mp:
            break
        scales.append((k, out_w, out_h))
        k += 1
    return scales, k_current


class ResolutionSelectorZerohackz:
    """Three-output node: width, height, length (frames).

    Widgets:
        orientation — landscape (default) or portrait
        megapixels  — resolution tier from 0.2 MP to 2.0 MP
        duration    — seconds, 2–10 (default 5)
    """

    @classmethod
    def INPUT_TYPES(cls):
        mp_options = list(RESOLUTIONS.keys())
        return {
            "required": {
                "orientation": (["landscape", "portrait"], {"default": "landscape"}),
                "megapixels": (mp_options, {"default": "0.4 (864x480)"}),
                "duration": ("INT", {"default": 5, "min": 2, "max": 10, "step": 1}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT")
    RETURN_NAMES = ("width", "height", "length")
    FUNCTION = "resolve"
    CATEGORY = "MiniMax H3/ZeroHackz"
    DESCRIPTION = ("MiniMax H3 resolution + duration picker."
                   "Outputs width, height, and frame count as integers.")

    def resolve(self, orientation, megapixels, duration):
        w, h = RESOLUTIONS[megapixels]
        if orientation == "portrait":
            w, h = h, w
        length = snap_frames(duration * FPS)
        return (w, h, length)


class ImageRatioSelectorZerohackz:
    """From an image, output width/height/length at exact ratio scales.

    Wire an image in, pick a scale stop with the slider, and the node
    outputs dimensions that preserve the exact W:H ratio while staying
    divisible by 32. Every offered scale is at or below 2 megapixels.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {
                    "tooltip": "Source image whose ratio is preserved."}),
                "scale_stop": ("INT", {
                    "default": 0, "min": 0, "max": 10, "step": 1,
                    "tooltip": "Pick a scale from the menu (all ≤ 2 MP). "
                               "Higher = bigger."}),
                "duration": ("INT", {
                    "default": 5, "min": 2, "max": 10, "step": 1}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "length", "info")
    FUNCTION = "resolve"
    CATEGORY = "MiniMax H3/ZeroHackz"
    DESCRIPTION = ("Exact-ratio image scaler for MiniMax H3. "
                   "All outputs are multiples of 32.")

    def resolve(self, image, scale_stop, duration):
        h_img, w_img = int(image.shape[1]), int(image.shape[2])
        scales, k_orig = _exact_ratio_scales(w_img, h_img)
        idx = max(0, min(scale_stop, len(scales) - 1))
        k, w, h = scales[idx]
        mp = w * h / 1_000_000

        lines = ["Source: %dx%d  |  %d scales  |  slider: %d/%d" %
                 (w_img, h_img, len(scales), idx, len(scales) - 1), ""]
        for i, (sk, sw, sh) in enumerate(scales):
            smp = sw * sh / 1_000_000
            marker = " ◄ current" if i == idx else ""
            tag = " [original]" if sk == k_orig else ""
            lines.append("  %d: %dx%d  (%.2f MP)%s%s" %
                         (i, sw, sh, smp, tag, marker))

        info = "\n".join(lines)
        LOG.info("ImageRatio: %dx%d → %dx%d (%.2f MP, k=%d)",
                 w_img, h_img, w, h, mp, k)
        length = snap_frames(duration * FPS)
        return (w, h, length, info)


NODE_CLASS_MAPPINGS = {
    "ResolutionSelectorZerohackz": ResolutionSelectorZerohackz,
    "ImageRatioSelectorZerohackz": ImageRatioSelectorZerohackz,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResolutionSelectorZerohackz": "MiniMax H3 Resolution Selector (ZeroHackz)",
    "ImageRatioSelectorZerohackz": "MiniMax H3 Ratio from Image (ZeroHackz)",
}
