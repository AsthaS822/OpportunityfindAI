from typing import List, Dict, Any, Union
from ..schemas.response import DiscoverResponse, VerificationMetadata, AlternativeSchema
from ..schemas.opportunity import OpportunitySchema, DecisionAnalysisSchema, EligibilityAnalysisSchema
from ..models.opportunity import InternalOpportunity
from ..utils.helpers import format_timestamp


class ResponseBuilder:
    def build_response(
        self,
        query: str,
        language: str,
        opportunities: Union[List[InternalOpportunity], List[Dict[str, Any]]],
        gemini_analysis: Dict[str, Any],
        thinking_steps: List[str],
        timings: Dict[str, int],
        additional_data: Dict[str, Any] = None,
    ) -> DiscoverResponse:
        opp_schemas = []
        live_verified_count = 0
        additional_data = additional_data or {}

        for opp in opportunities:
            if isinstance(opp, dict):
                vstatus = opp.get("verification", {}).get("status", "")
                if "Live Verified" in vstatus or "Verified" in vstatus:
                    live_verified_count += 1
                da = opp.get("decision_analysis") or {}
                ea = da.get("eligibility_analysis") or {}
                opp_schemas.append(OpportunitySchema(
                    id=opp.get("id"),
                    title=opp.get("title", "N/A"),
                    provider=opp.get("provider", "N/A"),
                    country=opp.get("country"),
                    category=opp.get("category", "Scholarship"),
                    degree=opp.get("degree"),
                    funding_type=opp.get("funding_type") or opp.get("funding"),
                    deadline=opp.get("deadline"),
                    eligibility=opp.get("eligibility"),
                    description=opp.get("description"),
                    official_url=opp.get("official_url"),
                    verification=opp.get("verification", {}),
                    source_type=opp.get("source_type") or opp.get("source", "Dataset Only"),
                    dataset_deadline=opp.get("dataset_deadline"),
                    live_deadline=opp.get("live_deadline"),
                    using_deadline=opp.get("live_deadline") or opp.get("deadline"),
                    dataset_ranking=opp.get("dataset_ranking"),
                    live_ranking=opp.get("live_ranking"),
                    match_score=opp.get("match_score"),
                    decision_analysis=DecisionAnalysisSchema(
                        eligibility=da.get("eligibility"),
                        suitability=da.get("suitability"),
                        difficulty=da.get("difficulty"),
                        confidence=da.get("confidence"),
                        recommendation=da.get("recommendation"),
                        risk=da.get("risk"),
                        overall_recommendation=da.get("overall_recommendation"),
                        why_recommended=da.get("why_recommended"),
                        why_not_fit=da.get("why_not_fit"),
                        overview=da.get("overview"),
                        who_can_apply=da.get("who_can_apply"),
                        required_qualification=da.get("required_qualification"),
                        minimum_cgpa=da.get("minimum_cgpa"),
                        required_experience=da.get("required_experience"),
                        documents_required=da.get("documents_required"),
                        funding_details=da.get("funding_details"),
                        application_process=da.get("application_process"),
                        selection_process=da.get("selection_process"),
                        application_fees=da.get("application_fees"),
                        official_deadline=da.get("official_deadline"),
                        official_source=da.get("official_source"),
                        verified_date=da.get("verified_date"),
                        application_link=da.get("application_link"),
                        status=da.get("status"),
                        eligibility_analysis=EligibilityAnalysisSchema(**ea) if ea else None,
                    ) if da else None,
                    eligibility_checks=opp.get("eligibility_checks"),
                    next_steps=opp.get("next_steps"),
                ))
            else:
                if "Live Verified" in (opp.verification or {}).get("status", ""):
                    live_verified_count += 1
                opp_schemas.append(OpportunitySchema(
                    id=opp.id,
                    title=opp.title,
                    provider=opp.provider,
                    country=opp.country,
                    category=opp.category,
                    degree=opp.degree,
                    funding_type=opp.funding_type,
                    deadline=opp.deadline,
                    eligibility=opp.eligibility,
                    description=opp.description,
                    official_url=opp.verified_url or opp.official_url,
                    verification=opp.verification,
                    source_type=opp.source_type,
                    dataset_deadline=opp.dataset_deadline,
                    live_deadline=opp.live_deadline,
                    using_deadline=opp.live_deadline or opp.dataset_deadline,
                    dataset_ranking=opp.dataset_ranking,
                    live_ranking=opp.live_ranking,
                    match_score=opp.match_score,
                ))

        verification = VerificationMetadata(
            status="Live Verified" if live_verified_count > 0 else "Dataset Only",
            sources_checked=len(opportunities),
            official_sources=live_verified_count,
        )

        official_links = []
        for opp in opportunities:
            url = opp.get("official_url") if isinstance(opp, dict) else (opp.verified_url or opp.official_url)
            if url and url != "Unknown":
                official_links.append(url)

        alts = []
        for a in additional_data.get("alternatives", []):
            alts.append(AlternativeSchema(**a))

        ai_available = gemini_analysis.get("ai_available", True)

        return DiscoverResponse(
            query=query,
            language=language,
            thinking_steps=thinking_steps,
            summary=gemini_analysis.get("summary", additional_data.get("summary", "No summary available.")),
            roadmap=gemini_analysis.get("roadmap", []),
            opportunities=opp_schemas,
            verification_summary=verification,
            official_links=list(set(official_links)),
            timings=timings,
            generated_at=format_timestamp(),
            intent=additional_data.get("intent"),
            missing_information=additional_data.get("missing_info"),
            total_found=additional_data.get("total_found"),
            verified_count=additional_data.get("verified_count"),
            decision_summary=additional_data.get("summary"),
            follow_up_questions=additional_data.get("follow_up_questions"),
            follow_up_required=additional_data.get("follow_up_required", False),
            ai_explanation_available=ai_available,
            alternatives=alts or None,
            action_checklist=gemini_analysis.get("action_checklist"),
            preparation_tips=gemini_analysis.get("preparation_tips"),
        )


response_builder = ResponseBuilder()
