# {{ORCHESTRATOR_NAME}} — design

> Design doc scaffold per ADR-068a site-discoverability template.
> Pattern source: `~/Documents/Github/platform-docs/04-decision-memory/adrs/ADR-068a-site-discoverability-orchestration.md`.

<!-- self-consistency closing-pass: counts re-derived + denominators verified + vocab merged + glossary grep clean — TODO at first publish per §27.6 -->

## §0 Summary

- **Vendor**: {{VENDOR_NAME}} (`{{API_BASE_URL}}`).
- **Pattern**: registry-as-IaC declarative YAML + Python reconciler.
- **Sibling references**: Glitchtip orchestrator (`vps_host/scripts/glitchtip-orchestrator/`,
  commit `83a04df`), Mailcow orchestrator (`vps_host/scripts/mailcow-orchestrator/`,
  commit `e04e612`), site-discoverability orchestrator
  (`vps_host/scripts/site-discoverability/`).
- **Universal rules embedded**: §27 append-only, §27.5 closure-claim live-probe,
  §29 confirmation triangle, §43.6 verify-before-claim, §43.7 names-not-evidence,
  §52 unattended-mode.

## §1 Context

Describe the operational gap this orchestrator closes. Cite the prior manual
process and the recurrence pattern that motivated lifting it into
registry-as-IaC.

## §2 Architecture

```
operator authors registry.yml
        |
        v
+----------------------+        +------------------------+
| {{ORCHESTRATOR_NAME}} | -----> | {{VENDOR_NAME}} REST API |
| reconcile / apply    | <----- |   ({{API_BASE_URL}})   |
+----------------------+        +------------------------+
        |
        v
writeback: entity_id + last_reconciled
```

### Subcommands

| Subcommand | Effect | §29 gating |
|---|---|---|
| `reconcile` | Read-only diff registry ↔ live | None (idempotent) |
| `apply` | Create missing `desired_state: live` entities | `--confirm` required |
| `list-live` | Dump live entities (sanity check) | None |

## §3 Registry schema

| Field | Owner | Notes |
|---|---|---|
| `name` | operator | Canonical identifier (matches docs/runbooks) |
| `slug` | operator | URL-safe identifier matching live API |
| `desired_state` | operator | `live` \| `tbd` \| `paused` \| `remove` |
| `entity_id` | reconciler | Populated from live API; never inferred |
| `last_reconciled` | reconciler | ISO8601-UTC timestamp of last successful reconcile |

Forward-compat: unknown YAML keys are preserved in `extras` so future schemas
can extend the row without breaking older readers.

## §4 Failure modes

(Operator-authored; fill in after first reconcile pass.)

## §5 Activation gates

(Per-{{ENTITY_NAME}} operator-OOB requirements before flipping `desired_state`
from `tbd` to `live`.)

## §6 Open questions

(Author here; close before §-publish-checklist stamp.)

## §-publish-checklist

<!-- §27.6: counts re-derived + denominators verified + vocab merged + glossary grep clean — stamp at first publish -->
- [ ] §0 summary entity-count matches §3 registry row count
- [ ] No vocabulary drift between §2 architecture and §3 schema
- [ ] All terms-of-art (`registry-as-IaC`, `reconcile`, `apply`, `confirmation
      triangle`, `live-probe`) defined in §0 or cross-referenced to universal §-source
- [ ] `<!-- closing-pass: ISO8601-UTC -->` stamp appended on publish
