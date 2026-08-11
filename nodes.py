"""
ResolutionSelector_Zerohackz

Single node that outputs width, height, and frame count for MiniMax H3.
Pick orientation, megapixels, and duration; the node handles the resolution
lookup, aspect flip, and 17k+5 frame grid snapping for you.
"""

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


def snap_frames(n):
    """Snap a frame count up to MiniMax H3's 17k+5 grid."""
    while n % 17 != 5:
        n += 1
    return n


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


NODE_CLASS_MAPPINGS = {
    "ResolutionSelectorZerohackz": ResolutionSelectorZerohackz,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResolutionSelectorZerohackz": "MiniMax H3 Resolution Selector (ZeroHackz)",
}
