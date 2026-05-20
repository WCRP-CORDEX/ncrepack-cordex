#! /usr/bin/env python3
# -*-python-*-
# Core functions for check_cmip7_packing
from math import prod
import numpy as np
import pyfive

class ParseError(Exception):
    """When any exception prevents pyfive from parsing the file."""
    pass


def check_cmip7_packing(filename):
    """Check if a filename passes the CMIP7 packing checks.

    Parameters
    ----------
    filename: str or path
        Path to a HDF5/netCDF file.

    Returns 
    -------
    result : bool
        Whether the file passes the checks
    reason : str
        An explanation of the result.

    Raises
    ------
    ParseError
        If any exception is raised during the file parsing by pyfive.
    """
    four_MiB = 4 * (2**20)

    # Open the file with pyfive
    try:
        f = pyfive.File(filename)
    except Exception:
        raise ParseError()

    # Check for consolidated internal metadata
    try:
        if not f.consolidated_metadata:
            return False, f"FAIL: File {filename!r} does not have consolidated internal metadata"
    except Exception:
        raise ParseError()

    if "time" in f:
        # Check for the time coordinates variable having one chunk
        t = f["time"]
        chunks = t.chunks
        if chunks is not None and t.id.get_num_chunks() > 1:
            # At least two chunks
            return False, (
                f"FAIL: File {filename!r} time coordinates variable "
                f"'time' has {t.id.get_num_chunks()} chunks "
                "(expected 1 chunk or contiguous)"
            )

        # Check for the time bounds variable having one chunk
        if "bounds" in t.attrs:
            bounds = str(np.array(t.attrs["bounds"]).astype("U"))
            if bounds in f:
                b = f[bounds]
                chunks = b.chunks
                if chunks is not None and b.id.get_num_chunks() > 1:
                    # At least two chunks
                    return False, (
                        f"FAIL: File {filename!r} time bounds variable "
                        f"{bounds!r} has {b.id.get_num_chunks()} chunks "
                        "(expected 1 chunk or contiguous)"
                    )

    # Check for the data variable having one chunks of at least ~4MiB
    if "variable_id" in f.attrs:
        variable_id = str(np.array(f.attrs["variable_id"]).astype("U"))
        if variable_id in f:
            d = f[variable_id]
            if chunks is not None and d.id.get_num_chunks() > 1:
                # At least two chunks
                chunks = d.chunks
                wordsize = d.dtype.itemsize
                chunksize = prod(chunks) * wordsize

                lee_way = 0
                if len(chunks) > 1:
                    lee_way = prod(chunks[1:]) * wordsize

                if chunksize + lee_way < four_MiB:
                    return False, (
                        f"FAIL: File {filename!r} data variable "
                        f"{variable_id!r} has uncompressed chunk size "
                        f"{chunksize} B (expected at least "
                        f"{four_MiB - lee_way} B or 1 chunk "
                        "or contiguous)"
                    )

    # Still here? Then the file has passed all of the checks.
    return True, f"PASS: File {filename!r}"