# Execution Policy Precedence

While the No-LLM Implementation Programme is active, its stricter sequential-delivery controls refine the general concurrency allowance in `conductor/autonomy.json`.

1. Use one active implementation branch and one active phase checkpoint.
2. Do not start the next functional slice until the current pull request has required checks, exact-tree merge evidence, synchronized `master`, branch cleanup, and a clean worktree.
3. At most one disposable checkout may exist for bounded review or reproduction. It never creates a second implementation lane.
4. External, credential, human, licence, rights, publication, and model-execution gates release the active slot; independent work continues only after the current slice is safely integrated or durably handed off.
5. If this programme ends or is superseded by an explicit owner decision, the general lane limits resume.

This precedence narrows concurrency only. It does not widen authority or weaken any safety, privacy, evidence, or external-effect gate.
