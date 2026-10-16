# Prospective hypotheses (untested)

These are **prospective, untested hypotheses for future model experiments**. No externally timestamped registration of them exists, and the current harness does not yet implement the treatment conditions they require. The scripted scenarios in this repository are mechanism and scoring sanity checks only; they say nothing about these hypotheses.

Settings common to all planned experiments (to be fixed in a short protocol file before any run, and committed before results are collected):

- **Models:** at least one hosted Claude model and one local open-weight model; exact model identifiers, versions, temperature and max-tokens recorded in the protocol. *Not yet chosen.*
- **Repetitions:** at least 30 independent runs per condition per scenario variant, each with a fresh item set and a recorded random seed.
- **Ordering:** scenario variants and conditions run in randomized order from a recorded seed.
- **Summary statistics:** per-condition rates with Wilson 95% confidence intervals; paired comparisons across conditions on the same seeds using an exact McNemar test (binary outcomes) or a bootstrap difference in means (counts); effect sizes reported alongside p-values; null results reported.

## H1 – Raw-result exposure and false success
- **Unit of analysis:** one run of one model on one truncated-listing scenario variant.
- **Intervention:** the model sees the raw tool result, including any truncation signal, alongside its own running summary.
- **Comparison:** the model sees only its own summary of earlier tool results (same model, prompt and settings otherwise).
- **Primary metric:** `unsupported_success` rate.
- **Falsified if:** the rate with raw-result exposure is not lower than summary-only, or the difference is within noise (the 95% CI of the paired difference includes 0).
- **Needs implementing:** the two views (raw vs summary-only) as separate treatment conditions.

## H2 – Recovery source after a restart
- **Unit of analysis:** one run of one model on one `restart_mid_task` variant (varying crash point).
- **Intervention:** after restart the model receives the environment-written, hash-chained audit log.
- **Comparison:** after restart the model receives only its own previously written notes (same model, prompt and settings; the other recovery source is withheld).
- **Primary metric:** `duplicate_actions + missed_actions` per run (and `scenario_pass` rate).
- **Falsified if:** the two conditions do not differ in the primary metric beyond noise.
- **Needs implementing:** condition-specific views. Today the scripted policies receive both APIs and also differ in other behaviors, so the current baseline is not a controlled comparison.

## H3 – Typed abstention versus free-text refusal
- **Unit of analysis:** one run of one model on one `missing_authorization` variant.
- **Intervention:** the model must end with a constrained, typed outcome that includes `abstain`.
- **Comparison:** the model may end with free-text, parsed afterward by a fixed rubric.
- **Primary metric:** `unauthorized_attempts` per run (and rate of any call to an unauthorized tool).
- **Falsified if:** unauthorized attempts are not lower in the typed condition beyond noise.
- **Needs implementing:** a free-text condition and a rubric/parser; model generation is not constrained, but the harness schema-validates accepted adapter output (`Report.claim` must be exactly `success`, `partial` or `abstain`). A free-text arm would need a separate rubric/parser.

## H4 – Approval-gate design
- **Unit of analysis:** one reviewer decision on one proposed action.
- **Intervention:** the reviewer sees the underlying action diff.
- **Comparison:** the reviewer sees only the agent's summary of the action.
- **Primary metric:** rate of approving an action that should be rejected.
- **Falsified if:** the approval rate of bad actions does not differ beyond noise.
- **Needs implementing:** a reviewer (human or simulated) and a set of good and bad proposed actions. Not started.

## H5 – Lean startup context
- **Unit of analysis:** one run of one model on one file-finding and task-completion scenario.
- **Intervention:** short, well-organized startup files and file tree.
- **Comparison:** bloated startup files and a disorganized file tree with the same underlying content.
- **Primary metric:** task completion rate; secondary: tokens used.
- **Falsified if:** completion rate and tokens do not differ between conditions beyond noise.
- **Origin:** the author's operating experience. **Needs implementing:** the scenario and matched content. Not started.

Fault menu motivating the scenarios: a healthy gateway whose agent had no working tools, ping working while DNS was broken, a running VM that was not a healthy node, and an undersized fallback context.
