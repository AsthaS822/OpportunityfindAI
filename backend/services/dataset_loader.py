import os
import uuid
import pandas as pd
import json
from typing import List
from ..models.opportunity import InternalOpportunity
from ..utils.logger import get_logger

from ..config import DATASET_PATH

logger = get_logger(__name__)

class DatasetLoader:
    def __init__(self):
        self.dataset_path = DATASET_PATH
        self.opportunities: List[InternalOpportunity] = []
        self.stats = {
            "files_loaded": 0,
            "files_ignored": 0,
            "row_breakdown": {}
        }

    def load_all(self):
        logger.info(f"Starting recursive dataset loading from: {self.dataset_path}")
        if not os.path.exists(self.dataset_path):
            logger.error(f"Dataset path does not exist: {self.dataset_path}")
            return

        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                file_path = os.path.join(root, file)
                self._load_file(file_path)
                
        logger.info("=== Dataset Loading Summary ===")
        logger.info(f"Total datasets: {self.stats['files_loaded']}")
        logger.info(f"Total opportunities: {len(self.opportunities)}")
        logger.info(f"Ignored files: {self.stats['files_ignored']}")
        for fname, count in self.stats['row_breakdown'].items():
            logger.info(f"  - {fname}: {count} rows")
        logger.info("===============================")

    def _load_file(self, file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == '.csv':
                self._load_csv(file_path)
            elif ext == '.json':
                self._load_json(file_path)
            elif ext == '.xlsx':
                self._load_xlsx(file_path)
            else:
                self.stats["files_ignored"] += 1
                logger.warning(f"Unsupported file format ignored: {file_path}")
        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")

    def _map_row(self, row: dict, source_file: str) -> InternalOpportunity:
        # Simple heuristic mapping for potentially varying columns
        def get_val(keys: List[str]):
            for k in keys:
                if k in row and pd.notna(row[k]) and str(row[k]).strip() != "":
                    return str(row[k]).strip()
            return None

        title = get_val(["title", "Name", "Opportunity Name", "Scholarship Name"]) or "Unknown Opportunity"
        provider = get_val(["provider", "University", "Organization", "Institution"]) or "Unknown Provider"
        country = get_val(["country", "Location", "Region"])
        category = get_val(["category", "Type", "Opportunity Type"]) or "Scholarship"
        degree = get_val(["degree", "Level", "Degree Level"])
        funding_type = get_val(["funding", "Funding Type", "Value"])
        deadline = get_val(["deadline", "Application Deadline", "End Date"])
        eligibility = get_val(["eligibility", "Requirements"])
        description = get_val(["description", "Details", "About"])
        official_url = get_val(["official_url", "URL", "Link", "Website"])

        # Determine default dataset ranking if present
        dataset_ranking = get_val(["ranking", "QS Ranking", "World Rank"])

        return InternalOpportunity(
            id=str(uuid.uuid4()),
            title=title,
            provider=provider,
            country=country,
            category=category,
            degree=degree,
            funding_type=funding_type,
            deadline=deadline,
            eligibility=eligibility,
            description=description,
            official_url=official_url,
            source_dataset=os.path.basename(source_file),
            dataset_deadline=deadline,
            dataset_ranking=dataset_ranking
        )

    def _load_csv(self, file_path: str):
        logger.info(f"Loading CSV: {file_path}")
        df = pd.read_csv(file_path)
        count = 0
        for _, row in df.iterrows():
            self.opportunities.append(self._map_row(row.to_dict(), file_path))
            count += 1
        self.stats["files_loaded"] += 1
        self.stats["row_breakdown"][os.path.basename(file_path)] = count

    def _load_json(self, file_path: str):
        logger.info(f"Loading JSON: {file_path}")
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    self.opportunities.append(self._map_row(item, file_path))
                    count += 1
            elif isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list):
                        for item in v:
                            if isinstance(item, dict):
                                self.opportunities.append(self._map_row(item, file_path))
                                count += 1
        self.stats["files_loaded"] += 1
        self.stats["row_breakdown"][os.path.basename(file_path)] = count

    def _load_xlsx(self, file_path: str):
        logger.info(f"Loading XLSX: {file_path}")
        df = pd.read_excel(file_path)
        count = 0
        for _, row in df.iterrows():
            self.opportunities.append(self._map_row(row.to_dict(), file_path))
            count += 1
        self.stats["files_loaded"] += 1
        self.stats["row_breakdown"][os.path.basename(file_path)] = count

dataset_loader = DatasetLoader()
