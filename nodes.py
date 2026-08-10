"""
ResolutionSelector_Zerohackz

Single node that outputs width, height, and frame count for MiniMax H3.
Pick orientation, quality, and duration; the node handles the resolution
lookup, aspect flip, and 17k+5 frame grid snapping for you.
"""

RESOLUTIONS = {
    "360P": (736, 416),
    "480P": (864, 480),
    "720P": (1344, 768),
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
        quality     — 360P, 480P (default), 720P
        duration    — seconds, 2–10 (default 5)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "orientation": (["landscape", "portrait"], {"default": "landscape"}),
                "quality": (["360P", "480P", "720P"], {"default": "480P"}),
                "duration": ("INT", {"default": 5, "min": 2, "max": 10, "step": 1}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT")
    RETURN_NAMES = ("width", "height", "length")
    FUNCTION = "resolve"
    CATEGORY = "ResolutionSelector_Zerohackz"
    DESCRIPTION = ("Quick resolution + duration picker for MiniMax H3. "
                   "Outputs width, height, and frame count as integers.")

    def resolve(self, orientation, quality, duration):
        w, h = RESOLUTIONS[quality]
        if orientation == "portrait":
            w, h = h, w
        length = snap_frames(duration * FPS)
        return (w, h, length)


NODE_CLASS_MAPPINGS = {
    "ResolutionSelectorZerohackz": ResolutionSelectorZerohackz,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResolutionSelectorZerohackz": "Resolution Selector (Zerohackz)",
}
