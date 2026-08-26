# Analysis module

This directory contains the initial, data-agnostic implementation for Anna
Sokolova's response-completeness workstream.

## Files

- `inspect_tahoe.py`: memory-conscious structural inventory for H5AD and
  Parquet inputs. It reports schemas and metadata fields without loading the
  full expression matrix.
- `response_completeness.py`: baseline condition-level estimators for robust
  response magnitude, DMSO-calibrated residual fraction/coverage, Wilson
  intervals, and dispersion change.
- `../docs/RESPONSE_COMPLETENESS.md`: scientific specification, validation
  design, terminology, assumptions, and limitations.

## Important boundary

The metric functions require a documented one-dimensional per-cell response
score. They intentionally do not choose genes, normalize counts, or fit a
representation. Those choices must be made with plate-6 development data,
recorded, frozen, and then applied unchanged to plate 14.

No Tahoe-100M result is included here yet. The website's existing example is
illustrative demo data and must not be interpreted as evidence.

## Inventory usage

```bash
python analysis/inspect_tahoe.py path/to/file.h5ad --output h5ad_inventory.json
python analysis/inspect_tahoe.py path/to/parquet_directory --format parquet \
  --output parquet_inventory.json
```

Do not commit credentials, raw cell-level data, controlled data, or large
inventory outputs containing sensitive identifiers.

## Metric usage

```python
from analysis.response_completeness import summarize_condition

result = summarize_condition(
    treated_scores=treated_score_vector,
    matched_control_scores=held_out_dmso_score_vector,
    calibration_control_scores=calibration_dmso_score_vector,
)
print(result.to_dict())
```

The held-out DMSO vector should also be passed as the "treated" vector in a
negative-control run to quantify DMSO-versus-DMSO behavior.

## Next steps after real-data inventory

1. Confirm plate, sample, drug, dose, cell-line, and DMSO coding.
2. Confirm independent DMSO sample identifiers on plates 6 and 14.
3. Select and document the plate-6 response representation.
4. Add sample-aware negative-control and quality-control analyses.
5. Export aggregate results compatible with `docs/schemas/result.schema.json`.
6. Apply the frozen configuration to matched plate-14 conditions.
