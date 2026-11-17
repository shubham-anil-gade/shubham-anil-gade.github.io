#!/usr/bin/env python3
"""Append eligible DOI records only. Dry-run by default; no scraping."""
import argparse
import datetime
import difflib
import html
import json
import re
import runpy
from urllib.parse import quote, urlencode
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
audit = runpy.run_path(str(ROOT / "scripts/audit-publications.py"))
ORCID = audit["ORCID"]
fetch, doi_key, title_key = (audit[k] for k in ("fetch", "doi_key", "title_key"))
MANUAL = ROOT / "src/data/publications.json"
SYNCED = ROOT / "src/data/synced-publications.json"
TYPES = {"journal-article": "Journal Article", "book-chapter": "Book Chapter"}

def clean(value):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", str(value or ""))).split())

def valid_doi(value):
    return bool(re.fullmatch(r"10\.\d{4,9}/[^\s<>]+", value))

def named_author(a):
    given = title_key(a.get("given", ""))
    return title_key(a.get("family", "")) == "gade" and given in {
        "shubham", "shubhama", "shubhamanil", "sa", "s"
    }

def same_orcid(a):
    return str(a.get("ORCID", "")).rstrip("/").rsplit("/", 1)[-1] == ORCID

def format_author(a):
    if named_author(a):
        return "Gade SA"
    family = clean(a.get("family"))
    given = clean(a.get("given"))
    initials = "".join(word[0].upper() for word in re.findall(r"[^\W\d_]+", given))
    if given.isupper() and given.isalpha() and len(given) <= 3:
        initials = given
    return (" ".join(x for x in (family, initials) if x) or clean(a.get("name")))

def openalex():
    records = []
    for page in range(1, 6):
        query = urlencode({"filter": f"authorships.author.orcid:{ORCID}",
                           "per_page": 100, "page": page,
                           "select": "doi,title,type"})
        response = fetch("https://api.openalex.org/works?" + query)
        batch = response["results"]
        records.extend({"doi": doi_key(x.get("doi") or ""), "title": x.get("title") or "",
                        "type": x.get("type")} for x in batch)
        if page * 100 >= response["meta"]["count"]:
            return records
    raise RuntimeError("OpenAlex result cap reached; review manually")

def duplicate(title, doi, records):
    target = title_key(title)
    for item in records:
        url = item["url"]
        if valid_doi(doi_key(url)) and doi_key(url) == doi:
            return "existing DOI"
        other = title_key(item["title"])
        if target == other:
            return "existing title"
        if min(len(target), len(other)) > 30 and (
            difflib.SequenceMatcher(None, target, other, autojunk=False).ratio() >= .88
            or (min(len(target), len(other)) / max(len(target), len(other)) >= .75
                and (target in other or other in target))
        ):
            return "similar title; manual review"
    return None

def candidate(work, doi, sources, existing, reviewed=False):
    if doi_key(work.get("DOI", "")) != doi:
        return None, "Crossref DOI mismatch"
    if work.get("type") not in TYPES:
        return None, "not an eligible journal article or book chapter"
    title = clean((work.get("title") or [""])[0])
    authors = work.get("author") or []
    if not title or not authors or any(not format_author(a) for a in authors):
        return None, "incomplete title or authors"
    if not any(named_author(a) and (same_orcid(a) or (not a.get("ORCID") and ("ORCID" in sources or reviewed))) for a in authors):
        return None, "authorship not sufficiently verified"
    relation = work.get("relation") or {}
    if any(relation.get(k) for k in ("is-preprint-of", "is-version-of", "is-replaced-by", "is-retraction-of", "is-correction-of")) or work.get("update-to") or work.get("updated-by"):
        return None, "related version, correction or update; review"
    reason = duplicate(title, doi, existing)
    if reason:
        return None, reason
    venue = clean((work.get("container-title") or [""])[0])
    if not venue:
        return None, "missing venue"
    year = None
    for k in ("published", "published-online", "published-print", "issued"):
        parts = ((work.get(k) or {}).get("date-parts") or [[]])[0]
        if parts and isinstance(parts[0], int):
            year = parts[0]
            break
    if not year or not 1900 <= year <= datetime.date.today().year + 1:
        return None, "invalid publication year"
    volume, issue = clean(work.get("volume")), clean(work.get("issue"))
    if volume:
        venue += ", " + volume + (f"({issue})" if issue else "")
    pages = clean(work.get("page") or work.get("article-number"))
    if pages:
        venue += ", " + ("pp. " if work["type"] == "book-chapter" else "") + pages
    return {"year": year, "title": title, "authors": ", ".join(format_author(a) for a in authors),
            "venue": venue, "type": TYPES[work["type"]], "url": "https://doi.org/" + doi,
            "linkLabel": "DOI"}, "eligible"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Append eligible entries")
    parser.add_argument("--reviewed-dois", default="", help="Comma-separated DOIs personally checked by repository owner")
    args = parser.parse_args()
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    synced = json.loads(SYNCED.read_text(encoding="utf-8"))
    existing = manual["publications"] + manual["preprints"] + synced
    reviewed = {doi_key(s) for s in args.reviewed_dois.split(",") if s.strip()}
    if any(not valid_doi(d) for d in reviewed) or len(reviewed) > 30:
        raise ValueError("Supply up to 30 valid comma-separated DOIs")
    report = {"sources": {}, "errors": {}, "eligible": [], "review": []}
    sources_by_doi = {}
    for source, method in (("ORCID", audit["from_orcid"]), ("Crossref", audit["from_crossref"]), ("OpenAlex", openalex)):
        try:
            records = method()
            report["sources"][source] = len(records)
            for r in records:
                doi = r.get("doi", "")
                if valid_doi(doi):
                    sources_by_doi.setdefault(doi, set()).add(source)
                elif r.get("title"):
                    report["review"].append({"title": r["title"], "source": source, "reason": "no DOI"})
        except Exception as exc:
            report["errors"][source] = str(exc)
    for doi in reviewed:
        sources_by_doi.setdefault(doi, set()).add("owner-reviewed DOI")
    known = {doi_key(r["url"]) for r in existing}
    for doi, sources in sorted(sources_by_doi.items()):
        if doi in known:
            continue
        try:
            work = fetch("https://api.crossref.org/works/" + quote(doi, safe="/"))["message"]
            row, reason = candidate(work, doi, sources, existing + report["eligible"], doi in reviewed)
            if row:
                report["eligible"].append(row)
            else:
                report["review"].append({"doi": doi, "sources": sorted(sources), "reason": reason})
        except Exception as exc:
            report["errors"][doi] = str(exc)
    Path("publication-sync-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    # Required sources or individual DOI failures block writes; optional discovery failure does not.
    if any(k != "OpenAlex" for k in report["errors"]):
        raise SystemExit("Required metadata retrieval failed; existing database unchanged.")
    if args.apply and report["eligible"]:
        SYNCED.write_text(json.dumps(synced + report["eligible"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
