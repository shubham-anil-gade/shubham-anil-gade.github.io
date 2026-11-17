import copy
import runpy
import unittest
from pathlib import Path

sync = runpy.run_path(str(Path(__file__).with_name("sync-publications.py")))
candidate = sync["candidate"]
DOI = "10.1234/test-publication"
WORK = {
    "DOI": DOI, "type": "journal-article",
    "title": ["A new study of irrigation management"],
    "author": [{"given": "Shubham Anil", "family": "Gade", "ORCID": sync["ORCID"]},
               {"given": "Jane", "family": "Example"}],
    "container-title": ["Example Journal"],
    "published": {"date-parts": [[2026]]}
}

class SyncTests(unittest.TestCase):
    def test_eligible(self):
        result, reason = candidate(WORK, DOI, {"Crossref"}, [])
        self.assertEqual(reason, "eligible")
        self.assertEqual(result["authors"], "Gade SA, Example J")
        self.assertEqual(result["url"], "https://doi.org/" + DOI)

    def test_duplicate_doi(self):
        row, reason = candidate(WORK, DOI, {"Crossref"}, [
            {"title": "Other title", "url": "https://doi.org/" + DOI.upper()}])
        self.assertIsNone(row)
        self.assertEqual(reason, "existing DOI")

    def test_duplicate_title(self):
        row, reason = candidate(WORK, DOI, {"Crossref"}, [
            {"title": WORK["title"][0].upper(), "url": "https://doi.org/10.1234/other"}])
        self.assertIsNone(row)
        self.assertEqual(reason, "existing title")

    def test_preprint(self):
        work = dict(WORK, type="posted-content")
        self.assertIsNone(candidate(work, DOI, {"ORCID"}, [])[0])

    def test_wrong_author(self):
        work = copy.deepcopy(WORK)
        work["author"][0]["ORCID"] = "different-author"
        self.assertIsNone(candidate(work, DOI, {"ORCID"}, [], True)[0])

    def test_missing_venue(self):
        self.assertIsNone(candidate(dict(WORK, **{"container-title": []}), DOI, {"Crossref"}, [])[0])

    def test_manual_doi(self):
        work = copy.deepcopy(WORK)
        del work["author"][0]["ORCID"]
        self.assertIsNone(candidate(work, DOI, {"OpenAlex"}, [])[0])
        self.assertIsNotNone(candidate(work, DOI, {"owner-reviewed DOI"}, [], True)[0])

    def test_related_version(self):
        work = dict(WORK, relation={"is-version-of": [{"id": "10.1234/old"}]})
        self.assertIsNone(candidate(work, DOI, {"ORCID"}, [])[0])

if __name__ == "__main__":
    unittest.main()
