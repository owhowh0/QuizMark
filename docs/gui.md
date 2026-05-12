# GUI Integration Guide

QuizMark keeps a stable JSON schema for GUI tooling.

## Recommended workflow

1. Load `.qm` via the Python API
2. Convert to JSON with `Quiz.to_json()`
3. Use validation errors for UI feedback
4. Persist back to `.qm` after edits
