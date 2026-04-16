import json
import logging
from typing import List, Dict, Any
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.llm = LLMService()

    async def generate_ai_insights(self, sessions_data: List[Dict[str, Any]], chat_histories: Dict[str, List[Dict[str, str]]]) -> Dict[str, Any]:
        schema = {
            "developer_insights": [
                {
                    "developer_id": "string",
                    "employee_name": "string",
                    "question_complexity_score": 5,
                    "question_severity": "Medium"
                }
            ],
            "topic_distribution": [
                {
                    "topic": "string",
                    "percentage": 50.0
                }
            ],
            "lagging_developer": {
                "developer_id": "string",
                "risk_summary": "string"
            }
        }
        
        prompt = (
            "Act as a Senior HR/Engineering Analyst. Evaluate the following developers' "
            "onboarding progress and chat logs to produce a strict JSON output matching the requested schema.\n"
            "For 'question_complexity_score', use an integer 1-10 assessing technical depth.\n"
            "For 'question_severity', use 'Low', 'Medium', or 'High' (e.g. asking about simple login is Low, asking about infrastructure blockers is High).\n"
            "For 'topic_distribution', break down the topics discussed into percentages. Their sum must evaluate to 100.\n"
            "For 'lagging_developer', identify the single developer struggling most based on tone, delays vs progress. Provide exactly one sentence for risk_summary.\n\n"
            "Data to analyze:\n"
        )
        
        data_to_analyze = []
        for session in sessions_data:
            dev_id = session['id']
            chat = chat_histories.get(dev_id, [])
            chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat[-50:]]) # Limit history size just in case
            data_to_analyze.append({
                "developer_id": dev_id,
                "name": session['name'],
                "percent_complete": session['percent_complete'],
                "chat_log": chat_text if chat_text else "No messages"
            })
            
        prompt += json.dumps(data_to_analyze, indent=2)
        
        try:
            result = await self.llm.extract_structured(prompt, schema)
            
            if "developer_insights" not in result:
                result["developer_insights"] = []
            if "topic_distribution" not in result:
                result["topic_distribution"] = []
                
            return result
        except Exception as e:
            logger.error(f"Failed to generate AI insights: {e}")
            return {
                "developer_insights": [],
                "topic_distribution": [],
                "lagging_developer": None
            }
