#!/usr/bin/env python3
"""Read-only publication audit; never changes the website."""
import json, re, unicodedata
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode, unquote

ORCID = "0000-0003-1671-8394"
ROOT = Path(__file__).resolve().parents[1]

def fetch(url, accept="application/json"):
    with urlopen(Request(url, headers={"Accept": accept, "User-Agent": "AcademicWebsitePublicationAudit/1.0"}), timeout=30) as response:
        return json.load(response)

def title_key(value):
    return "".join(c for c in unicodedata.normalize("NFKD", value).casefold() if c.isalnum())

def doi_key(value):
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", unquote(value.strip()), flags=re.I).lower()

def existing():
    manual = json.loads((ROOT / "src/data/publications.json").read_text(encoding="utf-8"))
    synced = json.loads((ROOT / "src/data/synced-publications.json").read_text(encoding="utf-8"))
    records = []
    for item in manual["publications"] + manual["preprints"] + synced:
        url = item["url"]
        records.append({"title": item["title"], "doi": doi_key(url) if re.match(r"https?://(?:dx\.)?doi\.org/", url, re.I) else ""})
    if not records:
        raise RuntimeError("No existing publication records recognized; aborting.")
    return records

def from_orcid():
    data = fetch(f"https://pub.orcid.org/v3.0/{ORCID}/works", "application/vnd.orcid+json")
    records = []
    for group in data["group"]:
        for work in group.get("work-summary", []):
            title = ((work.get("title") or {}).get("title") or {}).get("value", "")
            identifiers = (work.get("external-ids") or {}).get("external-id", [])
            dois = [doi_key(x["external-id-value"]) for x in identifiers
                    if x.get("external-id-type", "").lower() == "doi"
                    and x.get("external-id-relationship") == "self" and x.get("external-id-value")]
            year = (((work.get("publication-date") or {}).get("year") or {}).get("value"))
            if title:
                for doi in dois or [""]:
                    records.append({"title": title, "doi": doi, "year": year, "type": work.get("type")})
    return records

def from_crossref():
    records, offset = [], 0
    while True:
        params = urlencode({"filter": f"orcid:{ORCID}", "rows": 100, "offset": offset})
        data = fetch("https://api.crossref.org/works?" + params)["message"]
        for work in data["items"]:
            title = (work.get("title") or [""])[0]
            year = ((work.get("published") or {}).get("date-parts") or [[None]])[0][0]
            if title:
                records.append({"title": title, "doi": doi_key(work.get("DOI", "")), "year": year, "type": work.get("type")})
        offset += len(data["items"])
        if not data["items"] or offset >= data["total-results"]:
            break
        if offset >= 1000:
            raise RuntimeError("Unexpected result count; inspect manually.")
    return records

def compare(records, current):
    titles = {title_key(x["title"]) for x in current}
    dois = {x["doi"] for x in current if x["doi"]}
    result = {"already_listed": [], "candidates": []}
    seen = set()
    for item in records:
        key = item["doi"] or title_key(item["title"])
        if key in seen:
            continue
        seen.add(key)
        bucket = "already_listed" if (item["doi"] and item["doi"] in dois) or title_key(item["title"]) in titles else "candidates"
        result[bucket].append(item)
    return result

def main():
    current = existing()
    report = {"website_records_compared": len(current), "sources": {}, "errors": {}}
    for name, function in (("ORCID", from_orcid), ("Crossref", from_crossref)):
        try:
            report["sources"][name] = compare(function(), current)
        except Exception as exc:
            report["errors"][name] = str(exc)
    Path("publication-audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Existing website records compared: {len(current)}")
    for source, result in report["sources"].items():
        print(f"{source}: {len(result['already_listed'])} matched; {len(result['candidates'])} candidates (review required)")
        for item in result["candidates"]:
            print(f"  {item['year']} | {item['type']} | {item['title']} | {item['doi']}")
    for source, error in report["errors"].items():
        print(f"{source} unavailable: {error}")
    if report["errors"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
