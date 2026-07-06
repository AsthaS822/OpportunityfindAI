from typing import List
from rapidfuzz import fuzz
from ..models.opportunity import InternalOpportunity
from ..utils.logger import get_logger

logger = get_logger(__name__)

class Deduplicator:
    def deduplicate(self, opportunities: List[InternalOpportunity], threshold: float = 85.0) -> List[InternalOpportunity]:
        unique_opps: List[InternalOpportunity] = []
        
        for opp in opportunities:
            is_duplicate = False
            for u_opp in unique_opps:
                # If titles and providers are very similar, consider it a duplicate
                title_similarity = fuzz.ratio(opp.title.lower(), u_opp.title.lower())
                provider_similarity = fuzz.ratio(opp.provider.lower(), u_opp.provider.lower())
                
                if title_similarity > threshold and provider_similarity > threshold:
                    is_duplicate = True
                    # Optional: We could merge fields here, but for now just take the highest scored one
                    break
                    
            if not is_duplicate:
                unique_opps.append(opp)
                
        logger.info(f"Deduplication: {len(opportunities)} -> {len(unique_opps)}")
        return unique_opps

deduplicator = Deduplicator()
