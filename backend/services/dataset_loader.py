"""
Dataset Loader — loads, parses, and indexes opportunities from local files.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..models.opportunity import InternalOpportunity
from ..config import DATASET_PATH
from ..utils.logger import get_logger
import hashlib

logger = get_logger(__name__)

XLSX_AVAILABLE = False
try:
    import openpyxl
    XLSX_AVAILABLE = True
except ImportError:
    pass


class DatasetLoader:
    def __init__(self):
        self.opportunities: List[InternalOpportunity] = []
        self.stats: Dict[str, Any] = {
            "files_loaded": 0,
            "total_opportunities": 0,
            "ignored_files": 0,
        }

    def load_all(self, path: Optional[Path] = None) -> None:
        path = path or DATASET_PATH
        if not path.exists():
            logger.error(f"Dataset path not found: {path}")
            return

        logger.info(f"Starting recursive dataset loading from: {path}")
        all_opportunities: List[InternalOpportunity] = []
        total_files = 0
        ignored = 0

        for file_path in sorted(path.iterdir()):
            if not file_path.is_file():
                continue
            suffix = file_path.suffix.lower()
            if suffix not in (".xlsx", ".json", ".csv"):
                ignored += 1
                continue

            try:
                loaded = self._load_file(file_path)
                if loaded:
                    all_opportunities.extend(loaded)
                    logger.info(f"  - {file_path.name}: {len(loaded)} rows")
                total_files += 1
            except Exception as e:
                logger.error(f"  - {file_path.name}: ERROR: {e}")

        self.opportunities = all_opportunities
        self.stats = {
            "files_loaded": total_files,
            "total_opportunities": len(all_opportunities),
            "ignored_files": ignored,
        }

        logger.info("=== Dataset Loading Summary ===")
        logger.info(f"Total datasets: {total_files}")
        logger.info(f"Total opportunities: {len(all_opportunities)}")
        logger.info(f"Ignored files: {ignored}")
        logger.info("===============================")

    def _load_file(self, file_path: Path) -> List[InternalOpportunity]:
        suffix = file_path.suffix.lower()
        if suffix == ".xlsx":
            return self._load_xlsx(file_path)
        elif suffix == ".json":
            return self._load_json(file_path)
        elif suffix == ".csv":
            return self._load_csv(file_path)
        return []

    def _load_xlsx(self, file_path: Path) -> List[InternalOpportunity]:
        if not XLSX_AVAILABLE:
            logger.warning("openpyxl not installed — skipping XLSX")
            return []
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            wb.close()
            return []

        # Find the header row (first row with 3+ non-None values)
        header_idx = 0
        for i, row in enumerate(rows):
            non_none = sum(1 for v in row if v is not None)
            if non_none >= 3:
                header_idx = i
                break

        headers = [str(h).lower().strip() if h else f"col_{j}" for j, h in enumerate(rows[header_idx])]
        results = []
        for row in rows[header_idx + 1:]:
            if not any(v is not None for v in row):
                continue
            record = {}
            for i, val in enumerate(row):
                if i < len(headers):
                    record[headers[i]] = str(val).strip() if val is not None else ""
            opp = self._record_to_opportunity(record, file_path.name)
            if opp:
                results.append(opp)
        wb.close()
        return results

    def _load_json(self, file_path: Path) -> List[InternalOpportunity]:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        # Handle nested JSON: if dict, find the first list value (likely the records)
        if isinstance(data, dict):
            records = None
            for v in data.values():
                if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                    records = v
                    break
            if records is None:
                records = [data]
        else:
            records = data if isinstance(data, list) else [data]

        results = []
        for record in records:
            if isinstance(record, dict):
                opp = self._record_to_opportunity(record, file_path.name)
                if opp:
                    results.append(opp)
        return results

    def _load_csv(self, file_path: Path) -> List[InternalOpportunity]:
        results = []
        with open(file_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                opp = self._record_to_opportunity(dict(row), file_path.name)
                if opp:
                    results.append(opp)
        return results

    def _record_to_opportunity(self, record: Dict[str, str], source: str) -> Optional[InternalOpportunity]:
        title = self._get_field(record, ["title", "name", "institution name", "institution_name", "scheme_name", "scholarship name", "opportunity name", "program name", "scholarship_name"])
        if not title or len(title.strip()) < 3:
            return None

        opp_id = hashlib.md5(f"{source}_{title}".encode()).hexdigest()[:12]

        return InternalOpportunity(
            id=opp_id,
            title=title,
            provider=self._get_field(record, ["provider", "institution", "institution name", "university", "organization", "host institution", "funding organization", "award"]),
            country=self._get_field(record, ["country", "location", "host country", "study country", "location name"]),
            category=self._get_field(record, ["category", "type", "classification", "classification name", "scholarship type", "opportunity type", "schemeCategory"]),
            degree=self._get_field(record, ["degree", "degree level", "level", "study level", "education level"]),
            funding_type=self._get_field(record, ["funding type", "funding", "scholarship type", "financial coverage", "award"]),
            deadline=self._get_field(record, ["deadline", "application deadline", "closing date", "due date"]),
            eligibility=self._get_field(record, ["eligibility", "eligibility criteria", "requirements", "who can apply"]),
            description=self._get_field(record, ["description", "details", "about", "overview", "summary", "benefits", "details"]),
            official_url=self._get_field(record, ["official url", "url", "link", "website", "application link", "more info"]),
            source_dataset=source,
        )

    def _get_field(self, record: Dict[str, str], possible_keys: List[str]) -> str:
        for key in possible_keys:
            val = record.get(key) or record.get(key.lower()) or record.get(key.replace(" ", "_")) or ""
            if val and str(val).strip():
                return str(val).strip()
        return ""


dataset_loader = DatasetLoader()
