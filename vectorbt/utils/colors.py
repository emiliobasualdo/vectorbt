"""Utilities for working with colors."""

import numpy as np


def rgb_from_cmap(cmap_name, value, value_range):
    """Map `value_range` to colormap with name `cmap_name` and get RGB of the `value` from that range."""
    import matplotlib.pyplot as plt

    if value_range[0] == value_range[1]:
        norm_value = 0.5
    else:
        norm_value = (value - value_range[0]) / (value_range[1] - value_range[0])
    cmap = plt.get_cmap(cmap_name)
    return "rgb(%d,%d,%d)" % tuple(np.round(np.asarray(cmap(norm_value))[:3] * 255))


def adjust_opacity(color, opacity):
    """Adjust opacity of color."""
    import matplotlib.colors as mc

    rgb = mc.to_rgb(color)
    return 'rgba(%d,%d,%d,%.4f)' % (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), opacity)


def adjust_lightness(color, amount=0.7):
    """Lightens the given color by multiplying (1-luminosity) by the given amount.

    Input can be matplotlib color string, hex string, or RGB tuple.
    Output will be an RGB string."""
    import matplotlib.colors as mc
    import colorsys

    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    rgb = colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
    return 'rgb(%d,%d,%d)' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))