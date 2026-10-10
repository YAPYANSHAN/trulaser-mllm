# Evaluation results

Data: `jobs.csv`, split: random, test jobs: 225, LLM: offline-rules

## Defect classification (modality ablation)

| Model | Accuracy | Macro-F1 | ECE (lower is better) |
|---|---|---|---|
| table model only | 0.658 | 0.385 | 0.264 |
| image model only | 0.964 | 0.911 | 0.028 |
| video model only | 0.853 | 0.826 | 0.050 |
| table + image, conflict-aware fusion | 0.964 | 0.909 | 0.098 |
| simple average fusion (all) | 0.933 | 0.861 | 0.130 |
| conflict-aware fusion (all) | 0.969 | 0.915 | 0.105 |

## Abstention (answer 'unknown' when unsure)

Thresholds: min confidence 0.75, max conflict 0.70

- Coverage (share answered): 0.791
- Accuracy on answered jobs: 0.983
- Share of 'unknown' cases where the best guess would have been wrong: 0.0851

## Confusion matrix (fused, rows = true)

```
                      ok  dross rough_ incomp burn_o bevel_
              ok      64      0      0      0      0      0
           dross       0     30      0      0      0      0
rough_striations       5      0     18      0      0      0
  incomplete_cut       0      0      0      8      0      0
burn_overheating       1      0      0      0      1      0
 bevel_deviation       1      0      0      0      0     97
```

## Diagnosis reports

- {'reports': 5, 'schema_and_rule_valid_rate': 1.0, 'root_causes_with_evidence_rate': 0.75, 'mean_attempts': 1.0}

### job_id = J01278  (true: rough_striations, diagnosis: unknown, 2.71 s)

Root causes: 

Actions: re_measure_part, inspect_or_replace_nozzle, manual_review_by_engineer

Parameter changes: {}

Problems: none

### job_id = J01008  (true: incomplete_cut, diagnosis: incomplete_cut, 0.64 s)

Root causes: power_too_low ['E1'], dirty_protective_glass ['E2']

Actions: adjust_laser_power, clean_or_replace_protective_glass

Parameter changes: {'laser_power_w': {'from': 1753.77, 'to': 1986.83}}

Problems: none

### job_id = J00746  (true: bevel_deviation, diagnosis: unknown, 0.45 s)

Root causes: 

Actions: re_measure_part, inspect_or_replace_nozzle, manual_review_by_engineer

Parameter changes: {}

Problems: none

### job_id = J00102  (true: bevel_deviation, diagnosis: bevel_deviation, 0.58 s)

Root causes: bevel_axis_drift []

Actions: 

Parameter changes: {}

Problems: none

### job_id = J00871  (true: bevel_deviation, diagnosis: bevel_deviation, 0.76 s)

Root causes: bevel_axis_drift ['E2']

Actions: recalibrate_bevel_axis

Parameter changes: {}

Problems: none
