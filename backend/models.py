"""
データモデル定義
小学・幼児教育研究プラットフォーム用
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class AgeGroup(Enum):
    """年齢グループ"""
    INFANT = "幼児"  # 3-5歳
    LOWER_ELEMENTARY = "低学年"  # 6-8歳
    UPPER_ELEMENTARY = "高学年"  # 9-12歳


class Subject(Enum):
    """科目"""
    JAPANESE = "国語"
    MATH = "算数"
    SCIENCE = "理科"
    SOCIAL = "社会"
    ENGLISH = "英語"
    ART = "図工"
    MUSIC = "音楽"
    PE = "体育"


class SkillCategory(Enum):
    """スキルカテゴリ"""
    READING = "読解力"
    WRITING = "作文力"
    CALCULATION = "計算力"
    LOGICAL_THINKING = "論理的思考"
    CREATIVITY = "創造力"
    COMMUNICATION = "コミュニケーション"
    MOTOR_SKILLS = "運動能力"


@dataclass
class Student:
    """児童データモデル"""
    id: str
    name: str
    age: int
    age_group: AgeGroup
    grade: Optional[int] = None  # 幼児はNone
    enrollment_date: datetime = field(default_factory=datetime.now)


@dataclass
class LearningRecord:
    """学習記録"""
    id: str
    student_id: str
    subject: Subject
    score: float  # 0-100
    duration_minutes: int
    date: datetime
    skill_scores: dict = field(default_factory=dict)


@dataclass
class LearningMaterial:
    """教材データ"""
    id: str
    title: str
    subject: Subject
    age_group: AgeGroup
    difficulty: int  # 1-5
    skills: List[SkillCategory]
    description: str
    duration_estimate: int  # 分


@dataclass
class ProgressReport:
    """進捗レポート"""
    student_id: str
    period_start: datetime
    period_end: datetime
    subject_scores: dict
    skill_progress: dict
    recommendations: List[str]
    overall_growth: float


@dataclass
class AnalysisResult:
    """分析結果"""
    student_id: str
    analysis_date: datetime
    learning_patterns: dict
    strengths: List[str]
    areas_for_improvement: List[str]
    predicted_performance: dict
    personalized_tips: List[str]
