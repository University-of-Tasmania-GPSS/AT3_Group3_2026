"""Shared map-drawing helpers (basemap, real coordinates, scale bar, north arrow).

Rasters are drawn in their own projected coordinates (EPSG:7855, metres) so
axes show eastings/northings, not pixel counts. The basemap is Esri World
Topographic Map; tiles are downloaded on first use and cached locally.
"""
import textwrap
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import contextily as cx
import xyzservices.providers as providers
from matplotlib.colors import LightSource, ListedColormap, Normalize
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm


cx.set_cache_dir(Path.home() / ".cache" / "at3_tiles")

BASEMAP = providers.Esri.WorldTopoMap

# Risk classes (None + 5): "None" is transparent; the rest run light -> dark so the
# order survives greyscale and red-green colour blindness (magma_r; the range is wide so
# neighbouring classes stay at least ~14 lightness units apart). The highest class
# is also hatched.
RISK_COLOURS = plt.cm.magma_r(np.linspace(0.10, 0.92, 6))
HATCHED_FROM = 5
RISK_COLOURS[0, 3] = 0
RISK_CMAP = ListedColormap(RISK_COLOURS)


def raster_extent(transform, shape):
    """(left, right, bottom, top) for `imshow(extent=...)`."""
    height, width = shape
    left, top = transform * (0, 0)
    right, bottom = transform * (width, height)
    return left, right, bottom, top


def plot_hillshade(ax, dem, transform, nodata=None, azimuth=315, altitude=40, vert_exag=2):
    """Grey hillshade of `dem` as the map's base layer."""
    dem = np.ma.masked_equal(dem, nodata) if nodata is not None else np.ma.masked_invalid(dem)
    ls = LightSource(azdeg=azimuth, altdeg=altitude)
    shade = ls.hillshade(dem.filled(float(np.ma.median(dem))), vert_exag=vert_exag, dx=transform.a, dy=-transform.e)
    shade = np.ma.masked_where(dem.mask, shade)
    ax.imshow(shade, cmap="gray", vmin=0, vmax=1, extent=raster_extent(transform, dem.shape), zorder=0)


def add_scalebar(ax, length_m, label=None, loc="lower right"):
    """Black scale bar `length_m` metres long (axes must be in metres)."""
    bar = AnchoredSizeBar(
        ax.transData, length_m, label or f"{length_m / 1000:g} km", loc,
        pad=0.6, color="black", frameon=True, size_vertical=length_m / 60,
        fontproperties=fm.FontProperties(size=9),
    )
    bar.patch.set(facecolor="white", alpha=0.85, edgecolor="none")
    ax.add_artist(bar)


def add_north_arrow(ax, loc=(0.93, 0.93), size=0.09):
    """North arrow in axes coordinates (maps are north-up in a projected CRS)."""
    x, y = loc
    ax.annotate(
        "", xy=(x, y), xytext=(x, y - size), xycoords="axes fraction",
        arrowprops=dict(arrowstyle="-|>", color="black", lw=2, mutation_scale=18), zorder=10,
    )
    ax.text(x, y + 0.01, "N", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=12, fontweight="bold", zorder=10)


def style_map_axes(ax, crs_label="GDA2020 / MGA zone 55 (EPSG:7855)"):
    """Coordinate ticks in metres, light graticule, CRS named in the x-axis label."""
    fmt = FuncFormatter(lambda v, _: f"{v:,.0f}")
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(fmt)
    ax.tick_params(labelsize=8)
    ax.grid(color="white", alpha=0.5, lw=0.5, ls="--")
    ax.set_xlabel(f"Easting (m)  |  {crs_label}", fontsize=9)
    ax.set_ylabel("Northing (m)", fontsize=9)


def add_basemap(ax, bounds, margin=2000, crs="EPSG:7855", zoom=11):
    """Crop the map to `bounds` (xmin, ymin, xmax, ymax) plus `margin` metres
    and draw the Esri topographic basemap underneath. Call before plotting data."""
    x0, y0, x1, y1 = bounds
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(y0 - margin, y1 + margin)
    cx.add_basemap(ax, crs=crs, source=BASEMAP, zoom=zoom, attribution=False)
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(y0 - margin, y1 + margin)


def add_attribution(ax):
    """Basemap credit under the map (required by Esri)."""
    ax.figure.text(0.5, 0.005, "\n".join(textwrap.wrap(BASEMAP.attribution, 150)),
                   ha="center", va="bottom", fontsize=5.5, color="dimgrey")


def plot_risk(ax, risk_class, transform, nodata=255, alpha=0.78, hatch="///"):
    """Draw a classified risk raster (0 = None ... 5 = Very High). The Very High
    classes are hatched as well as coloured, so they stay distinct in greyscale and with
    colour blindness."""
    height, width = risk_class.shape
    left, right, bottom, top = raster_extent(transform, risk_class.shape)
    ax.imshow(np.ma.masked_equal(risk_class, nodata), cmap=RISK_CMAP, vmin=0, vmax=len(RISK_COLOURS) - 1,
              alpha=alpha, extent=(left, right, bottom, top), interpolation="nearest", zorder=2)
    xs = left + (np.arange(width) + 0.5) * transform.a
    ys = top + (np.arange(height) + 0.5) * transform.e
    cs = ax.contourf(xs, ys, ((risk_class >= HATCHED_FROM) & (risk_class != nodata)).astype(int), levels=[0.5, 1.5],
                     colors="none", hatches=[hatch], zorder=3)
    cs.set_edgecolor("white")
    cs.set_linewidth(0)


def risk_legend(ax, labels, title="Relative risk", loc="upper left"):
    """Legend for the classes in `labels` (first label, 'None', is left out)."""
    handles = [Patch(facecolor=RISK_COLOURS[i], edgecolor="white" if i >= HATCHED_FROM else "black",
                     linewidth=0.5, label=labels[i], hatch="///" if i >= HATCHED_FROM else None)
               for i in range(1, len(labels))]
    ax.legend(handles=handles, title=title, loc=loc, fontsize=8, title_fontsize=9, framealpha=0.95)


def plot_risk_continuous(ax, risk, transform, alpha=0.85):
    """Draw the continuous 0-1 risk score on a fixed 0-1 stretch (so the colours mean the
    same at every scale). Zero and no-data cells are left transparent. Returns the image,
    for `add_risk_colourbar`."""
    masked = np.ma.masked_where(~np.isfinite(risk) | (risk <= 0), risk)
    return ax.imshow(masked, cmap="magma_r", norm=Normalize(0, 1), alpha=alpha,
                     extent=raster_extent(transform, risk.shape), interpolation="nearest", zorder=2)


def add_risk_colourbar(ax, image, edges=(0.2, 0.4, 0.6, 0.8)):
    """Colourbar with ticks at 0, the class edges and 1, so it lines up with the classed maps."""
    cbar = ax.figure.colorbar(image, ax=ax, shrink=0.8, pad=0.02, label="Relative risk (0-1)")
    cbar.set_ticks([0, *edges, 1])
    return cbar


def label_values(ax, gdf, name_col, values, fmt="{:.2f}", fontsize=7):
    """Number each named system on the map and list 'number, name, value' in a key box
    (bottom left), so the value can be read without matching a colour to the colourbar.
    `values` is a Series indexed by name; numbers follow its order."""
    lines = ["Mean risk by named area"]
    for k, (name, value) in enumerate(values.items(), 1):
        geom = gdf.loc[gdf[name_col] == name].geometry.union_all()
        if geom.is_empty or not np.isfinite(value):
            continue
        point = geom.representative_point()
        ax.annotate(str(k), (point.x, point.y), ha="center", va="center", fontsize=fontsize, fontweight="bold",
                    bbox=dict(boxstyle="circle,pad=0.25", facecolor="white", edgecolor="black", linewidth=0.8),
                    zorder=6)
        lines.append(f"{k}  {name.replace('  ', ' ')}: {fmt.format(value)}")
    ax.text(0.01, 0.02, "\n".join(lines), transform=ax.transAxes, fontsize=fontsize - 0.5, va="bottom", ha="left",
            linespacing=1.4, bbox=dict(facecolor="white", alpha=0.92, edgecolor="grey", pad=4), zorder=10)


def score_colours(n, zero_transparent=True):
    """n colours for ordinal scores 0..n-1, light -> dark (same magma_r ramp as the risk maps).
    Score 0 is transparent by default so the basemap shows through."""
    colours = plt.cm.magma_r(np.linspace(0.10, 0.92, n))
    if zero_transparent:
        colours[0, 3] = 0
    return colours


def plot_scores(ax, array, transform, n, nodata=255, alpha=0.8, colours=None):
    """Draw an integer score raster (0..n-1) with `score_colours`, or with `colours` (n RGBA rows)
    where a class should be fainter, e.g. a background class that covers most of the map."""
    colours = score_colours(n) if colours is None else colours
    ax.imshow(np.ma.masked_equal(array, nodata), cmap=ListedColormap(colours), vmin=0, vmax=n - 1,
              alpha=alpha, extent=raster_extent(transform, array.shape), interpolation="nearest", zorder=2)


def scores_legend(ax, labels, title="Score", loc="upper left", extra_handles=(), colours=None, skip=(0,)):
    """Legend for `plot_scores`; scores in `skip` (default 0, transparent) are left out. Pass the same `colours`."""
    colours = score_colours(len(labels), zero_transparent=False) if colours is None else colours
    handles = [Patch(facecolor=colours[i], edgecolor="black", linewidth=0.5, label=labels[i])
               for i in range(len(labels)) if i not in skip]
    ax.legend(handles=handles + list(extra_handles), title=title, loc=loc, fontsize=8, title_fontsize=9,
              framealpha=0.95)


def data_bounds(mask, transform):
    """(xmin, ymin, xmax, ymax) of the True cells of a boolean array, for `add_basemap`."""
    rows, cols = np.where(mask)
    x0, y_top = transform * (cols.min(), rows.min())
    x1, y_bottom = transform * (cols.max() + 1, rows.max() + 1)
    return x0, y_bottom, x1, y_top


def finish_map(ax, scalebar_m=5000, scalebar_label=None):
    """Coordinate ticks, scale bar and north arrow in one call."""
    style_map_axes(ax)
    add_scalebar(ax, scalebar_m, scalebar_label)
    add_north_arrow(ax)
