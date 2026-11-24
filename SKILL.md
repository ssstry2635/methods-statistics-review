---
name: methods-statistics-review
description: Audit research design, analysis units, sample flow and statistical reporting with source-anchored checks and reproducible recalculation.
---

# 研究方法与统计审查

Version 1.0.0. Use actual sources and retain enough evidence to reproduce the judgment.

## Input and deliverables

Read the caller's arrangements before choosing an output format. In a mounted case environment, read /input/case.json, task.md and the resource inventory if present. Use /app/work for derived text and /app/output for final outputs; otherwise use the caller's locations. Read the actual document contents even when labels disagree. Preserve case_id and all original output_contract names, types, files and nesting. Use the normalized helper interface as a supplemental artifact. Save a truthful partial result early with identified materials, known status and specific gaps.

Build an inventory of manuscript, supplement, metadata, data and any reference actually allowed by the scope. Use available PDF text tools with original page boundaries. Verify extracted tables, symbols, footnotes, numeric precision and negation against the rendered page where the extraction is ambiguous. Preserve publisher page number or PDF page index, section/table/figure and a short verbatim anchor. You can create a UTF-8 extraction with stable lines for the mechanical checker, and bind those lines back to the original location. If a file is unreadable, record the attempted method and affected claims. External research must follow the task's scope.

### Methods and statistics
Build a design ledger before calling anything a defect. Record question and estimand, design, assignment unit, observation unit, inferential unit, repeated measures/clusters, analysis set and missingness. Record the outcome, time point and comparator for every check. Keep each comparison within the same cohort, estimand, analysis and unit. Identify alternative analyses and when their assumptions actually matter.

- Numerical checks: reconcile enrollment, exclusions and analysis denominators by group and time point. Count exclusions only once and account for overlapping reports and missingness. Check reported percentages in their actual precision. Preserve reported precision, formulas, inputs and matched source locations. For a comparable design and available data, document an independently rerunnable recomputation of the intended estimate, uncertainty or test. A failed simple consistency check is a discrepancy to trace, not evidence of misconduct.
- Inference checks: identify paired, clustered or repeated observations and verify how the reported model handles dependence. Separate missing detail from stated incompatible practice. Check prespecified versus exploratory outcomes, multiplicity families and missing-data handling. Interpret a confidence interval and p value together only if estimand, level, sidedness, test and adjustment match. Distinguish prospective power assumptions, realized precision and any post-hoc calculation.
- Deliver the requested facet-by-facet coverage and a short set of atomic findings. Include locations, status, category, severity, what inference changes and a concrete revision. For a reporting omission list the relevant sections actually reviewed and the information still required. Include defensible choices when they close a requested check.
- Normalize only defensible numeric checks to `examples/input.json`'s format and run `scripts/verify.py`. Set `applicable=false` with a reason for ambiguous comparisons. A consistent arithmetic result leaves design and scientific judgments for the reviewer.

## Final check

Run the checker from its installed directory using working-file paths. Read the output and reconcile it against the source, including units, comparison scope and uncertainties. Verify the requested check or item coverage before finishing. For each contested finding, consider one plausible alternative reading and state what resolves it or keeps it pending. Calibrate severity to scientific consequence. Keep judgment, reported fact, reproducible calculation and scope limits distinct. Distinguish missing material, inability to determine, and execution failure. Save the actual result, source and version mapping, uncertainty, normalized verification input and relevant change record as permitted by the output contract. Any required editable visual needs a rendered preview. Do not create a figure comparison without an original and an applicable target.
