# Skill Evaluation Methodology

Trigger evaluation uses separate training and held-out cases. Each case is run
at least three times against the exact client/model revision. Positive cases
require a trigger rate of 1.0 and negative cases require 0.0. Only training
failures may influence description changes before the held-out evaluation.

Output evaluation preserves every raw observation and evaluates named
assertions. All hard assertions must pass. An unavailable, blocked, malformed,
or unreviewed run is not a pass. Privacy or evidence-integrity failure blocks
promotion regardless of aggregate score.

Once a held-out case is evaluated, relabel it as exposed and never use it to
support a later held-out claim. A failure becomes an immutable regression case.
Any revised description must pass training and exposed regression cases before
one evaluation against a newly frozen held-out partition.

Receipts record the description, skill revision, client, model, parameters,
trial count, raw-result locations, assertion outcomes, nondeterminism,
limitations, and reviewer status. Existing H0-H8 results remain historical and
are not treated as comparable without Track 05 reconciliation.
