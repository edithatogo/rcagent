# PR 93 dependency admission check

The initial reviewed head was `e640c455a38dfefc879aa2ff7e0d54f0ca986d2f`.
A normal Renovate rebase request produced
`03f86e4691ae3ca733444b0fbed99ad2da4ac96d`. Both have tree
`36c59d4626bf76ecde684fafdcc445684b77c070`; the reviewed dependency bytes
are unchanged. Seven hosted checks pass on the refreshed head, including
three-platform Quality and patch coverage. `renovate/stability-days` remains
pending. The PR was not merged and no status or admission policy was overridden.

## Published version evidence

The read-only admission agent checked official upstream GitHub release
metadata and verified the proposed Action SHAs against their tags, peeling
the annotated Codecov tag. Publication timestamps are UTC.

| Dependency | Published | Seven-day admission boundary |
|---|---|---|
| actions/checkout v6.1.0 | 2026-07-20T15:23:28Z | 2026-07-27T15:23:28Z |
| actions/dependency-review-action v4.9.0 | 2026-03-03T22:21:10Z | 2026-03-10T22:21:10Z |
| actions/setup-python v6.3.0 | 2026-06-24T02:48:35Z | 2026-07-01T02:48:35Z |
| actions/upload-artifact v4.6.2 | 2025-03-19T17:47:02Z | 2025-03-26T17:47:02Z |
| actions/upload-artifact v7.0.1 | 2026-04-10T17:31:14Z | 2026-04-17T17:31:14Z |
| codecov/codecov-action v5.5.5 | 2026-06-09T01:02:35Z | 2026-06-16T01:02:35Z |
| vale-cli/vale-action 2.1.2 | 2026-05-18T19:35:12Z | 2026-05-25T19:35:12Z |
| actions/python-versions 3.13.15-31064747964 | 2026-08-06T02:29:25Z | 2026-08-13T02:29:25Z |

All listed releases satisfy the seven-day age policy. The remaining
`dtolnay/rust-toolchain@4360b525…` pin matches the upstream `stable` branch.
Its commit is dated 2026-08-05, but no corresponding release was found.
Commit age is not published-release age. A missing timestamp is a plausible
reason for the pending Renovate check, but inaccessible bot logs prevent
attributing the exact cause. Refresh did not clear the pending check.

## Continuing boundary

Keep PR 93 open until the bot's admission evidence is resolved. Do not make
timestamps optional, manufacture success, or promise a future unblock date.
Dashboard #74 lists the PR as open but supplies no per-dependency timestamp
diagnostic. The Mend log page returns an unauthenticated application shell
(`success:false`, `userSession:null`) through the current read-only session.
The next diagnostic input is the authenticated Mend job log for the refresh
that generated the pending status at 2026-08-31T13:00:24Z. It must establish
which dependency and release timestamp Renovate actually used; the cause and
an eventual expiry date are not established. GitHub credentials were not sent
to the separate service.
This admission check does not change Track 01's engineering scope or require
independent human review.
