#!/usr/bin/env python3
"""Memory-conscious inventory for Tahoe-100M H5AD or Parquet inputs.

This script reports structure only. It does not run a scientific analysis or
load an entire expression matrix into memory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def inspect_h5ad(path: Path) -> dict:
    try:
        import anndata as ad
    except ImportError as exc:
        raise SystemExit("Install anndata to inspect H5AD files") from exc

    obj = ad.read_h5ad(path, backed="r")
    try:
        return {
            "format": "h5ad",
            "path": str(path),
            "shape": list(obj.shape),
            "obs_columns": list(map(str, obj.obs.columns)),
            "var_columns": list(map(str, obj.var.columns)),
            "layers": list(map(str, obj.layers.keys())),
            "obsm": list(map(str, obj.obsm.keys())),
            "uns": list(map(str, obj.uns.keys())),
        }
    finally:
        if getattr(obj, "file", None) is not None:
            obj.file.close()


def inspect_parquet(path: Path) -> dict:
    try:
        import pyarrow.dataset as ds
    except ImportError as exc:
        raise SystemExit("Install pyarrow to inspect Parquet datasets") from exc

    dataset = ds.dataset(str(path), format="parquet")
    fragments = list(dataset.get_fragments())
    return {
        "format": "parquet",
        "path": str(path),
        "schema": str(dataset.schema),
        "fragment_count": len(fragments),
        "partitioning": str(dataset.partitioning),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--format", choices=("h5ad", "parquet"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    fmt = args.format
    if fmt is None:
        fmt = "h5ad" if args.path.suffix.lower() == ".h5ad" else "parquet"
    report = inspect_h5ad(args.path) if fmt == "h5ad" else inspect_parquet(args.path)
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
