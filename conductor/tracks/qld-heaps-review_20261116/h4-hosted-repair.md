# H4 first hosted attempt and portable FIFO test repair

The first H4 publication was `a9df9ba581eeeeae9a777546125225fae2c88b25`, tree
`c77bea38bcdb322c2d9b2d3f9d081e6a7f28b8fc`. Its
[Windows Quality job](https://github.com/edithatogo/rcagent/actions/runs/43957189042/job/133614737639)
failed before pytest: Windows-target ty correctly reported that `os` has no
`mkfifo` member. A runtime pytest platform-skip decorator did not make the direct
attribute reference valid for static analysis. This failed result is retained;
that head was not merged.

## Bounded repair

Only the test's FIFO capability lookup changed. It now obtains `mkfifo` with
`getattr`, verifies it is callable and explicitly skips on hosts without that
API before constructing fixtures. On supported hosts it still creates a real
synthetic FIFO with mode `0o600`, runs the actual CLI and requires exit 2.
No production source, schema, fixture expectation, test denominator, dependency,
CI gate, typing allowance or suppression changed. The H4 module still collects
220 tests.

| Test-file revision | SHA-256 |
| --- | --- |
| Original checkpoint | `5b794df73241730efca79cc3d5863b7fd765969e2955dfa2fd7c1081da36ffcb` |
| Portable repair | `03a83edfea642163de6e4f058df8abb68262e16af3586b78bca5f72eff161dfa` |

The author reproduced the diagnostic using
`uv run --no-sync ty check --python-platform win32 tests/test_heaps.py` before
editing. That command then passed. The integration lane additionally ran
`uv run --no-sync ty check --python-platform win32 tools tests`: all checks
passed. Ruff/format/basedpyright remained clean. The actual POSIX FIFO test passed
in both the author and separate read-only review lanes. The reviewer also
simulated an absent API and observed the intended skip before filesystem inputs
were created.

Both H4 production hashes remain unchanged from [the original review](./h4-review.md).
The earlier full local run, oracle execution and CLI replay are preserved with
their original test-file identity; they are not silently relabelled as a new run.
The [current input manifest](./h4-input-manifest.json) records the repaired test
bytes and links its previous exact revision. Fresh hosted checks on the new
publication head are required before merge; local target simulation is not a
hosted Windows pass.
