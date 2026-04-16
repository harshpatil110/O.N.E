from pydantic import BaseModel
from typing import List, Optional

class CompletionMatrixItem(BaseModel):
    developer_id: str
    employee_name: str
    percent_complete: int

class TaskVelocityItem(BaseModel):
    task_id: str
    title: str
    avg_duration_hours: float

class QuantitativeData(BaseModel):
    overall_completion: float
    completion_matrix: List[CompletionMatrixItem]
    task_velocity: List[TaskVelocityItem]

class DeveloperInsight(BaseModel):
    developer_id: str
    employee_name: str
    question_complexity_score: int
    question_severity: str

class TopicDistributionItem(BaseModel):
    topic: str
    percentage: float

class LaggingDeveloper(BaseModel):
    developer_id: str
    risk_summary: str

class SentimentIndexItem(BaseModel):
    employee_name: str
    frustration_score: int
    primary_emotion: str

class AutonomyScoreItem(BaseModel):
    employee_name: str
    independence_rating: int
    messages_per_task: float

class QualitativeData(BaseModel):
    developer_insights: List[DeveloperInsight]
    topic_distribution: List[TopicDistributionItem]
    lagging_developer: Optional[LaggingDeveloper] = None
    sentiment_index: List[SentimentIndexItem]
    autonomy_scores: List[AutonomyScoreItem]

class DeepDiveAnalyticsResponse(BaseModel):
    quantitative: QuantitativeData
    qualitative: QualitativeData
