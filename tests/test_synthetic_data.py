import csv
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_synthetic_data.py"
SPEC = importlib.util.spec_from_file_location("generator", SCRIPT)
generator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(generator)


class SyntheticDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        generator.write_outputs()
        with (ROOT / "data" / "synthetic_malaria_monthly.csv").open(encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_expected_number_of_records(self):
        self.assertEqual(len(self.rows), 12 * 24)

    def test_identifiers_have_dhis2_uid_length(self):
        self.assertTrue(all(len(row["org_unit_uid"]) == 11 for row in self.rows))
        self.assertTrue(all(len(uid) == 11 for uid in generator.DATA_ELEMENTS.values()))

    def test_core_validation_rules_pass(self):
        self.assertTrue(all(not generator.quality_flags(row) for row in self.rows))

    def test_data_is_aggregate_only(self):
        forbidden = {"name", "patient_id", "phone", "address", "latitude", "longitude"}
        self.assertTrue(forbidden.isdisjoint(self.rows[0].keys()))


if __name__ == "__main__":
    unittest.main()
