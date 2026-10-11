"""Upstream D8 counts that need the saved Whitebox pointer: how many of the cells draining to each
karst polygon fall inside a flagged zone (e.g. Karst Atlas proximal catchments).

Kept apart from `hydro.py` because it needs numba, which only the Stage 13 comparison uses.
"""

import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from numba import njit


@njit
def _receiver(pointer, index, height, width, nodata):
    """Flat index of the cell that `index` drains to (Whitebox-native D8 codes), or -1."""
    code = int(pointer[index])
    if code == nodata or code == 0:
        return -1
    row = index // width
    col = index - row * width
    if code == 1:
        row -= 1; col += 1
    elif code == 2:
        col += 1
    elif code == 4:
        row += 1; col += 1
    elif code == 8:
        row += 1
    elif code == 16:
        row += 1; col -= 1
    elif code == 32:
        col -= 1
    elif code == 64:
        row -= 1; col -= 1
    elif code == 128:
        row -= 1
    else:
        return -1
    if row < 0 or row >= height or col < 0 or col >= width:
        return -1
    receiver = row * width + col
    if pointer[receiver] == nodata:
        return -1
    return receiver


@njit
def _reverse_graph(pointer, height, width, nodata):
    head = np.full(pointer.size, -1, np.int32)
    nxt = np.full(pointer.size, -1, np.int32)
    for source in range(pointer.size):
        if pointer[source] == nodata:
            continue
        receiver = _receiver(pointer, source, height, width, nodata)
        if receiver >= 0:
            nxt[source] = head[receiver]
            head[receiver] = source
    return head, nxt


@njit
def _traverse(head, nxt, seeds, visited, stack, generation, flag):
    """Cells upstream of (and including) `seeds`, and how many of them are flagged."""
    size = 0
    total = 0
    flagged = 0
    for i in range(len(seeds)):
        seed = int(seeds[i])
        if visited[seed] != generation:
            visited[seed] = generation
            stack[size] = seed
            size += 1
    while size > 0:
        size -= 1
        current = stack[size]
        total += 1
        if flag[current]:
            flagged += 1
        upstream = head[current]
        while upstream >= 0:
            if visited[upstream] != generation:
                visited[upstream] = generation
                stack[size] = upstream
                size += 1
            upstream = nxt[upstream]
    return total, flagged


def upstream_flag_counts(pointer_path, targets, flag_path, id_col="OBJECTID"):
    """For each target polygon: upstream cells, and how many lie inside the flagged zone.

    `pointer_path`: Whitebox-native D8 pointer (as saved by the routing notebooks).
    `flag_path`: raster on the same grid, 1 where flagged (e.g. KPROXCATCH present).
    `targets`: polygons in the pointer's CRS.

    Returns one row per target with `target_cells`, `upstream_cells` and `upstream_flagged`
    (own cells removed from both, so these count water arriving from outside the polygon).
    """
    with rasterio.open(pointer_path) as src:
        nodata = int(src.nodata)
        pointer = src.read(1).astype(np.int16)
        transform = src.transform
        height, width = src.shape
    with rasterio.open(flag_path) as src:
        flag = (src.read(1) == 1).reshape(-1)
    valid = pointer != nodata
    pointer_flat = pointer.reshape(-1)
    head, nxt = _reverse_graph(pointer_flat, height, width, nodata)
    visited = np.zeros(pointer_flat.size, np.int32)
    stack = np.empty(pointer_flat.size, np.int32)

    rows = []
    for i, (target_id, geometry) in enumerate(zip(targets[id_col], targets.geometry)):
        minx, miny, maxx, maxy = geometry.bounds
        c0 = max(0, int(np.floor((minx - transform.c) / transform.a)))
        c1 = min(width, int(np.ceil((maxx - transform.c) / transform.a)) + 1)
        r0 = max(0, int(np.floor((transform.f - maxy) / abs(transform.e))))
        r1 = min(height, int(np.ceil((transform.f - miny) / abs(transform.e))) + 1)
        seeds = np.empty(0, np.int32)
        if r1 > r0 and c1 > c0:
            inside = rasterize([(geometry, 1)], out_shape=(r1 - r0, c1 - c0),
                               transform=transform * rasterio.Affine.translation(c0, r0),
                               fill=0, dtype="uint8").astype(bool) & valid[r0:r1, c0:c1]
            rr, cc = np.where(inside)
            seeds = ((r0 + rr) * width + c0 + cc).astype(np.int32)
        total = flagged = 0
        if len(seeds):
            total, flagged = _traverse(head, nxt, seeds, visited, stack, i + 1, flag)
            # remove the polygon's own cells: water arriving from outside only
            total -= len(seeds)
            flagged -= int(flag[seeds].sum())
        rows.append({id_col: target_id, "target_cells": len(seeds),
                     "upstream_cells": total, "upstream_flagged": flagged})
    return pd.DataFrame(rows)
