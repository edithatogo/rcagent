# No-LLM Implementation Programme

- **Status:** New
- **Type:** Chore / delivery programme
- **Scope:** Remaining work that does not require downloading model weights

## Track artefacts

- [Specification](./spec.md)
- [Implementation plan](./plan.md)
- [Metadata](./metadata.json)

## Operating rule

Use one active implementation branch and at most one disposable isolated
checkout. Merge each small PR only after its required checks pass, then delete
the merged branch and clean the disposable checkout before starting the next
slice.
