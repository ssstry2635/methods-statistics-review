import sys
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
import verify
from evidence import anchor, inventory, load

class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.examples = PROJECT / "examples"
        self.model = load(self.examples / "input.json")

    def test_a_quote_on_the_wrong_line_fails(self):
        sources, _ = inventory(self.examples, self.model["sources"])
        with self.assertRaisesRegex(ValueError, "Quote absent"):
            anchor({"source_id": "doc", "start": 1, "end": 1,
                    "quote": "a phrase never present"}, sources)

    def test_source_hash_detects_a_changed_file(self):
        self.model["sources"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            inventory(self.examples, self.model["sources"])

    def test_recalculates_disjoint_counts_and_rounded_percent(self):
        report = verify.audit(self.model, self.examples)
        flow, percent, dependence = report["checks"]
        self.assertEqual(flow["calculation"]["expected"], "95")
        self.assertEqual(flow["status"], "discrepancy")
        self.assertEqual(percent["status"], "consistent")
        self.assertEqual(dependence["status"], "uncertain")

    def test_missing_comparable_population_stays_unresolved(self):
        check = self.model["checks"][0]
        check.update(applicable=False, reason="Different analysis populations")
        check.pop("analyzed")
        self.assertEqual(verify.audit(self.model, self.examples)["checks"][0]["status"], "uncertain")

    def test_percentage_checks_rounding_boundaries(self):
        check = self.model["checks"][1]
        check.update(numerator=1, denominator=16, reported="6.3", places=1)
        self.assertTrue(verify.evaluate(check)[0])
        check.update(reported="6.4")
        self.assertFalse(verify.evaluate(check)[0])
