# ncrepack-cordex

`ncrepack-cordex` is a fork of [cmip7repack](https://github.com/NCAS-CMS/cmip7_repack) with slightly different default behaviour and to be used in CORDEX.

`cmip7repack` is a command-line tool for Unix-like platforms, bespoke
to CMIP, which can be used by the modelling groups, prior to dataset
publication, to "repack" their files (i.e. to re-organise the file
contents to have a different chunk and internal file metadata layout)
in such as way as to improve their read-performance over the lifetime
of the CMIP7 archive (note that CMIP7 datasets are written only once,
but read many times).

`check_cmip7_packing` is a command-line tool for Unix-like platforms,
bespoke to CMIP, which can be used to check if datasets have a
sufficiently good internal structure. Any dataset that has been
output by `cmip7repack` is guaranteed to pass the checks.

# Feature comparison

| Feature | `cmip7repack` | `ncrepack-cordex` |
|---------|:---:|:---:|
| Rechunk `time` coordinate to a single chunk | ✅ | ✅ |
| Rechunk time-bounds variable to a single chunk | ✅ | ✅ |
| Collate internal file metadata | ✅ | ✅ |
| Shuffle + zlib + Fletcher32 on rechunked vars | ✅ | ✅ |
| Size-based data variable rechunking (`-d`) | ✅ | ✅ |
| Minimal data variable chunk size is 4 MB | ✅ | ❌ |
| Custom chunk shape (`-c CHUNK`) | ❌ | ✅ |
| Filename-driven rechunking (`_1hr_` → 6, `_6hr_` → 4) | ❌ | ✅ |
| Default zlib compression level | 4 | 1 |

# `ncrepack-cordex` documentation

`ncrepack-cordex` is a copy of `cmip7repack` with a different default
policy for rechunking the main data variable (identified by the global
attribute `variable_id`).

### Default behavior

For the main data variable only:

* If the main data variable has uncompressed chunk sizes greater than
  4 MB, it is left untouched. Otherwise:
* Files with `_1hr_` in the filename are rechunked so that the first
  chunk dimension (time) is `6`.
* Files with `_6hr_` in the filename are rechunked so that the first
  chunk dimension (time) is `4`.
* All other files (day, mon) are left with the main data variable untouched.

In those filename-driven cases, only the first chunk dimension is
changed; all other chunk dimensions are preserved.

### Option precedence for main data variable

* `-c CHUNK` has highest priority and fully sets the chunk shape (for
  example `-c 6x50x50`).
* `-d SIZE` overrides the filename-driven defaults and uses the same
  size-based chunking algorithm as `cmip7repack`.
* If neither `-c` nor `-d` is provided, the filename-driven defaults
  are used.

### Compression default

`ncrepack-cordex` defaults to zlib deflation level `1`.
This can still be overridden with `-z`.

### Synopsis

```
ncrepack-cordex [-c chunk] [-d size] [-h] [-o] [-V] [-x] [-z n] FILE [FILE ...]
```

### Examples

```
# Filename-driven default: first chunk dimension set to 6
ncrepack-cordex file_1hr_frequency.nc

# Filename-driven default: first chunk dimension set to 4
ncrepack-cordex file_6hr_frequency.nc

# Override filename defaults with size-based behavior
ncrepack-cordex -d 8388608 file_1hr_frequency.nc

# Fully custom chunk shape
ncrepack-cordex -c 6x50x50 file.nc
```
        
# Citation

Hassell, D., & Cimadevilla Alvarez, E. (2026). cmip7repack: Repack CMIP7 netCDF-4 datasets. Zenodo. https://doi.org/10.5281/zenodo.17550919

# Installation

To install `ncrepack-cordex` and `ncrepack-cordex-check`, first install `cmip7-repack`, then
download the scripts with those names from this repository, give them executable
permissions, and make them available from a location in the `PATH`
environment variable.
To do this, the `install.sh` script is provided for convenience.

In summary:

```
conda install -c conda-forge cmip7-repack
bash <(curl -L https://wcrp-cordex.github.io/ncrepack-cordex/install.sh)
```