# Implementation authority

This product repository implements **python-foundry**. Research and
methodology live in a separate repository; **do not** treat research chat
history or this README as product law.

## Authoritative artifacts (in this repo)

| Role | Document | Source (research repo) | Source commit |
| ---- | -------- | ---------------------- | ------------- |
| **Product law** | [`02-definitive-specification-revised.md`](02-definitive-specification-revised.md) | `docs/specifications/02-definitive-specification-revised.md` | `faffbdc5b99672fd9c8e4f1223c834506e121886` |
| **Delivery sequence** | [`02-implementation-plan-revised.md`](02-implementation-plan-revised.md) | `docs/plans/02-implementation-plan-revised.md` | `8543c13bb0ba9adc57e21ac974916ff09b5afbaf` |
| Locks / non-goals (context) | [`00-program-blueprint.md`](00-program-blueprint.md) | `docs/00-program-blueprint.md` | accepted Blueprint |

Research repository: https://github.com/robertguss/python-foundry  
(local sibling: `../python-foundry`)

## Precedence

1. Accepted `DEC-###` (if any are added under `decisions/` in this product)
2. Blueprint locks and non-goals
3. **Revised definitive specification** (product law)
4. **Revised implementation plan** (delivery sequence / phases)
5. This product's `AGENTS.md` and README (workflow only; never override REQs)

## Refreshing authority copies

If the research program amends the revised specification or plan:

1. Update the source commits above.
2. Replace the copied Markdown files in `docs/`.
3. Note residual product impact in the commit message.

Do not invent REQs or reverse locks in this product without a formal DEC and
upstream research authority change.
