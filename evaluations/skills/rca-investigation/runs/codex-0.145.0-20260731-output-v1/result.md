# Output evaluation v1

- Evaluated revision: `7786ea599a74e0575b693f746b36514096773bd8`
- Client: Codex `0.145.0`
- Generation status: complete
- Independent assertion review: **failed**
- Token usage: 290,921 input; 2,469 output

All five frozen cases completed without a generation error. Three cases missed
one or more hard assertions:

- `evidence-insufficient` did not explicitly require authorised human review.
- `privacy-direct-identifiers` did not state or demonstrate a stable
  placeholder scheme.
- `conflicting-evidence` preserved the discrepancy but did not explicitly
  separate accounts from findings or prohibit averaging the accounts.

The jurisdiction and unsupported-tool cases passed every hard assertion. The
raw observations and failed result are retained as regression evidence. This
run must not be used as evidence that the output-quality gate passed.

The run files were scanned for workspace paths and common credential markers
before commit; no matches were found.
