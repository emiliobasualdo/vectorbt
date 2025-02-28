"""Utilities for images."""

import numpy as np
import imageio
from tqdm import tqdm
import plotly.graph_objects as go


def hstack_image_arrays(a, b):
    """Stack NumPy images horizontally."""
    h1, w1, d = a.shape
    h2, w2, _ = b.shape
    c = np.full((max(h1, h2), w1 + w2, d), 255, np.uint8)
    c[:h1, :w1, :] = a
    c[:h2, w1:w1 + w2, :] = b
    return c


def vstack_image_arrays(a, b):
    """Stack NumPy images vertically."""
    h1, w1, d = a.shape
    h2, w2, _ = b.shape
    c = np.full((h1 + h2, max(w1, w2), d), 255, np.uint8)
    c[:h1, :w1, :] = a
    c[h1:h1 + h2, :w2, :] = b
    return c


def save_animation(fname, index, plot_func, *args, delta=None, step=1,
                   fps=3, writer_kwargs=None, show_progress=True, **kwargs):
    """Save animation to a file.

    Args:
        fname (str): File name.
        index (iterable): Index to iterate over.
        plot_func (callable): Plotting function.

            Should take subset of `index`, `*args`, and `**kwargs`, and return either a Plotly figure,
            image that can be read by `imageio.imread`, or a NumPy array.
        *args: Positional arguments passed to `plot_func`.
        delta (int): Window size of each iteration.
        step (int): Step of each iteration.
        fps (int): Frames per second.
        writer_kwargs (dict): Keyword arguments passed to `imageio.get_writer`.
        show_progress (bool): Whether to show the progress bar.
        **kwargs: Keyword arguments passed to `plot_func`.
    """
    if writer_kwargs is None:
        writer_kwargs = {}
    if delta is None:
        delta = len(index) // 2

    with imageio.get_writer(fname, fps=fps, **writer_kwargs) as writer:
        for i in tqdm(range(0, len(index) - delta, step), disable=not show_progress):
            fig = plot_func(index[i:i + delta], *args, **kwargs)
            if isinstance(fig, (go.Figure, go.FigureWidget)):
                fig = fig.to_image(format="png")
            if not isinstance(fig, np.ndarray):
                fig = imageio.imread(fig)
            writer.append_data(fig)
