# CI Fails: ModuleNotFoundError for heic_converter - Add PYTHONPATH in workflow

## Issue Description
The CI job is failing because tests cannot import the heic_converter module (see: https://github.com/johnsirmon/pyExtractHEIC/actions/runs/22279887377/job/64448850222?pr=4). This can be fixed by setting the PYTHONPATH to the repo root in the 'Test (pytest)' workflow step.

## Suggested change:
```yaml
- name: Test (pytest)
  run: PYTHONPATH=. pytest --tb=short
```