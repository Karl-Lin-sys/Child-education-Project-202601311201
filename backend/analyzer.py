"""
学習データ分析モジュール
児童の学習パターン、成績推移、スキル発達を分析
"""
import statistics
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
from models import (
    Student, LearningRecord, AnalysisResult,
    Subject, SkillCategory, AgeGroup
)


class LearningAnalyzer:
    """学習データ分析エンジン"""
    
    def __init__(self, students: List[Student], records: List[LearningRecord]):
        self.students = {s.id: s for s in students}
        self.records = records
        self._build_indices()
    
    def _build_indices(self):
        """データインデックスを構築"""
        self.records_by_student = defaultdict(list)
        self.records_by_subject = defaultdict(list)
        
        for record in self.records:
            self.records_by_student[record.student_id].append(record)
            self.records_by_subject[record.subject].append(record)
    
    def analyze_student(self, student_id: str) -> Optional[AnalysisResult]:
        """個別児童の学習分析"""
        if student_id not in self.students:
            return None
        
        student = self.students[student_id]
        records = self.records_by_student[student_id]
        
        if not records:
            return None
        
        # 学習パターン分析
        learning_patterns = self._analyze_patterns(records)
        
        # 強みと改善点を特定
        strengths, improvements = self._identify_strengths_improvements(records)
        
        # 成績予測
        predictions = self._predict_performance(records)
        
        # パーソナライズされたアドバイス
        tips = self._generate_tips(student, records, strengths, improvements)
        
        return AnalysisResult(
            student_id=student_id,
            analysis_date=datetime.now(),
            learning_patterns=learning_patterns,
            strengths=strengths,
            areas_for_improvement=improvements,
            predicted_performance=predictions,
            personalized_tips=tips
        )
    
    def _analyze_patterns(self, records: List[LearningRecord]) -> Dict:
        """学習パターンを分析"""
        # 科目別平均スコア
        subject_scores = defaultdict(list)
        for r in records:
            subject_scores[r.subject.value].append(r.score)
        
        subject_averages = {
            subj: round(statistics.mean(scores), 1)
            for subj, scores in subject_scores.items()
        }
        
        # 学習時間分析
        total_minutes = sum(r.duration_minutes for r in records)
        avg_duration = statistics.mean([r.duration_minutes for r in records])
        
        # 成績推移（週別）
        weekly_scores = self._calculate_weekly_trend(records)
        
        # 集中力指標（学習時間と成績の相関）
        focus_index = self._calculate_focus_index(records)
        
        return {
            "subject_averages": subject_averages,
            "total_study_minutes": total_minutes,
            "average_session_minutes": round(avg_duration, 1),
            "weekly_score_trend": weekly_scores,
            "focus_index": focus_index,
            "total_sessions": len(records)
        }
    
    def _calculate_weekly_trend(self, records: List[LearningRecord]) -> List[Dict]:
        """週別成績推移を計算"""
        records_sorted = sorted(records, key=lambda r: r.date)
        if not records_sorted:
            return []
        
        weekly_data = defaultdict(list)
        for r in records_sorted:
            week_start = r.date - timedelta(days=r.date.weekday())
            week_key = week_start.strftime("%Y-%m-%d")
            weekly_data[week_key].append(r.score)
        
        return [
            {"week": week, "average_score": round(statistics.mean(scores), 1)}
            for week, scores in sorted(weekly_data.items())
        ]
    
    def _calculate_focus_index(self, records: List[LearningRecord]) -> float:
        """集中力指標を計算（0-100）"""
        if len(records) < 5:
            return 50.0
        
        # 学習時間と成績の相関を簡易計算
        durations = [r.duration_minutes for r in records]
        scores = [r.score for r in records]
        
        avg_duration = statistics.mean(durations)
        avg_score = statistics.mean(scores)
        
        # 効率スコア = 成績 / 学習時間
        efficiencies = [s / max(d, 1) for s, d in zip(scores, durations)]
        focus = min(100, statistics.mean(efficiencies) * 30)
        
        return round(focus, 1)
    
    def _identify_strengths_improvements(
        self, records: List[LearningRecord]
    ) -> tuple:
        """強みと改善点を特定"""
        # スキル別平均スコア
        skill_scores = defaultdict(list)
        for r in records:
            for skill, score in r.skill_scores.items():
                skill_scores[skill].append(score)
        
        skill_averages = {
            skill: statistics.mean(scores)
            for skill, scores in skill_scores.items()
        }
        
        if not skill_averages:
            return [], []
        
        avg_all = statistics.mean(skill_averages.values())
        
        strengths = [
            skill for skill, avg in skill_averages.items()
            if avg > avg_all + 10
        ]
        
        improvements = [
            skill for skill, avg in skill_averages.items()
            if avg < avg_all - 10
        ]
        
        return strengths[:3], improvements[:3]
    
    def _predict_performance(self, records: List[LearningRecord]) -> Dict:
        """成績予測"""
        records_sorted = sorted(records, key=lambda r: r.date)
        
        if len(records_sorted) < 10:
            return {"confidence": "low", "trend": "insufficient_data"}
        
        # 直近と過去の成績を比較
        half = len(records_sorted) // 2
        recent_avg = statistics.mean([r.score for r in records_sorted[half:]])
        past_avg = statistics.mean([r.score for r in records_sorted[:half]])
        
        growth_rate = (recent_avg - past_avg) / max(past_avg, 1) * 100
        
        if growth_rate > 5:
            trend = "improving"
            prediction = min(100, recent_avg * 1.05)
        elif growth_rate < -5:
            trend = "declining"
            prediction = max(0, recent_avg * 0.95)
        else:
            trend = "stable"
            prediction = recent_avg
        
        return {
            "trend": trend,
            "growth_rate": round(growth_rate, 1),
            "predicted_score": round(prediction, 1),
            "confidence": "high" if len(records) > 50 else "medium"
        }
    
    def _generate_tips(
        self,
        student: Student,
        records: List[LearningRecord],
        strengths: List[str],
        improvements: List[str]
    ) -> List[str]:
        """パーソナライズされたアドバイスを生成"""
        tips = []
        
        # 年齢に応じたアドバイス
        if student.age_group == AgeGroup.INFANT:
            tips.append("遊びを通じた学習を続けましょう。楽しさが一番大切です！")
        elif student.age_group == AgeGroup.LOWER_ELEMENTARY:
            tips.append("毎日少しずつ学習する習慣をつけましょう。")
        else:
            tips.append("目標を設定して、計画的に学習を進めましょう。")
        
        # 強みに基づくアドバイス
        if strengths:
            tips.append(f"「{strengths[0]}」が得意ですね！さらに伸ばしていきましょう。")
        
        # 改善点に基づくアドバイス
        if improvements:
            tips.append(f"「{improvements[0]}」を少しずつ練習してみましょう。")
        
        # 学習量に基づくアドバイス
        recent_records = [r for r in records if r.date > datetime.now() - timedelta(days=7)]
        if len(recent_records) < 5:
            tips.append("最近の学習回数が少なめです。毎日少しでも学習時間を作りましょう。")
        
        return tips
    
    def get_class_statistics(self) -> Dict:
        """クラス全体の統計"""
        all_scores = [r.score for r in self.records]
        
        if not all_scores:
            return {}
        
        # 科目別クラス平均
        subject_class_avg = {}
        for subject in Subject:
            subject_records = self.records_by_subject[subject]
            if subject_records:
                subject_class_avg[subject.value] = round(
                    statistics.mean([r.score for r in subject_records]), 1
                )
        
        # 年齢層別統計
        age_group_stats = {}
        age_records = defaultdict(list)
        for r in self.records:
            student = self.students.get(r.student_id)
            if student:
                age_records[student.age_group.value].append(r.score)
        
        for age_group, scores in age_records.items():
            age_group_stats[age_group] = {
                "average": round(statistics.mean(scores), 1),
                "count": len(scores)
            }
        
        return {
            "total_students": len(self.students),
            "total_records": len(self.records),
            "overall_average": round(statistics.mean(all_scores), 1),
            "subject_averages": subject_class_avg,
            "age_group_statistics": age_group_stats
        }
