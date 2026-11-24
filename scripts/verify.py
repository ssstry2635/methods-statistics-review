"""Recalculate explicitly comparable statistical reports and design checks."""
import argparse
from decimal import Decimal, InvalidOperation
from pathlib import Path

from evidence import anchor, dump, index, inventory, load, require

def decimal(value):
    require(type(value) in (str, int, float), "Expected a numeric value")
    result = Decimal(str(value))
    require(result.is_finite(), "Expected a finite number")
    return result

def count(value):
    result = decimal(value)
    require(result >= 0 and result == result.to_integral_value(), "Counts must be nonnegative integers")
    return result

def interval(value, places):
    require(type(places) is int and 0 <= places <= 12, "Invalid reported decimal places")
    number = decimal(value)
    half = Decimal(1).scaleb(-places) / 2
    return number - half, number + half

def evaluate(check):
    kind = check["kind"]
    if kind == "sample_flow":
        require(isinstance(check["disjoint_exclusions"], list), "Exclusions must be a list")
        enrolled = count(check["enrolled"])
        excluded = sum(count(x) for x in check["disjoint_exclusions"])
        expected = enrolled - excluded
        reported = count(check["analyzed"])
        return expected >= 0 and expected == reported, {"expected": str(expected), "reported": str(reported)}
    if kind == "percentage":
        numerator, denominator = map(count, (check["numerator"], check["denominator"]))
        require(0 < denominator and numerator <= denominator, "Invalid proportion")
        low, high = interval(check["reported"], check["places"])
        require(0 <= decimal(check["reported"]) <= 100, "Percentage must be in [0,100]")
        actual = numerator * 100
        return low * denominator <= actual <= high * denominator, {
            "ratio_percent": f"{actual}/{denominator}", "rounding_interval": [str(low), str(high)]}
    if kind == "interval_order":
        lo, hi = map(decimal, (check["lower"], check["upper"]))
        return lo <= hi, {"lower": str(lo), "upper": str(hi)}
    if kind == "p_range":
        p = decimal(check["p"])
        return 0 <= p <= 1, {"p": str(p)}
    if kind == "unit_independence":
        units = {check["inferential_unit"], check["analysis_unit"]}
        require(all(isinstance(x, str) and x.strip() for x in units), "Specify both units")
        adjustment = check["dependence_handling"]
        require(adjustment in {"none_explicit", "modeled", "unknown"}, "Specify dependence handling")
        if adjustment == "unknown" or adjustment == "modeled":
            return None, {"reason": "Review adequacy of dependence handling against design and model"}
        return len(units) == 1, {"inferential_unit": check["inferential_unit"],
                                 "analysis_unit": check["analysis_unit"]}
    raise ValueError(f"Unknown check kind: {kind}")

def audit(model, root):
    sources, metadata = inventory(root, model["sources"])
    rows = []
    for cid, check in index(model["checks"], "check").items():
        refs = [anchor(ref, sources) for ref in check["anchors"]]
        require(refs, f"Missing evidence: {cid}")
        scope = check["scope"]
        require(isinstance(scope, str) and scope.strip(), f"Missing population/endpoint scope: {cid}")
        if check.get("applicable") is not True:
            require(str(check.get("reason", "")).strip(), f"Missing applicability reason: {cid}")
            passed, detail = None, {"reason": check["reason"]}
        else:
            passed, detail = evaluate(check)
        rows.append({"id": cid, "kind": check["kind"], "scope": scope, "anchors": refs,
                     "status": "uncertain" if passed is None else "consistent" if passed else "discrepancy",
                     "calculation": detail})
    return {"case_id": model["case_id"], "sources": metadata, "checks": rows,
            "scope": "Mechanical checks of supplied transcriptions and applicability judgments."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        dump(args.out, audit(load(args.input), args.root))
    except (ValueError, KeyError, TypeError, OSError, InvalidOperation) as exc:
        dump(args.out, {"status": "input_or_execution_error", "detail": str(exc)})
        parser.exit(2, f"{exc}\n")

if __name__ == "__main__":
    main()
