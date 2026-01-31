"""
AI教材推薦エンジン
児童の学習状況に基づいて最適な教材を推薦
"""
from typing import List, Dict, Optional
from collections import defaultdict
import statistics
from models import (
    Student, LearningRecord, LearningMaterial,
    Subject, SkillCategory, AgeGroup
)


class MaterialRecommender:
    """教材推薦エンジン"""
    
    def __init__(
        self,
        students: List[Student],
        records: List[LearningRecord],
        materials: List[LearningMaterial]
    ):
        self.students = {s.id: s for s in students}
        self.materials = materials
        self.records_by_student = defaultdict(list)
        
        for record in records:
            self.records_by_student[record.student_id].append(record)
    
    def recommend_for_student(
        self,
        student_id: str,
        max_recommendations: int = 5
    ) -> List[Dict]:
        """個別児童への教材推薦"""
        if student_id not in self.students:
            return []
        
        student = self.students[student_id]
        records = self.records_by_student[student_id]
        
        # 学習履歴がない場合は年齢に応じた基本推薦
        if not records:
            return self._recommend_by_age(student, max_recommendations)
        
        # 学習分析に基づく推薦
        recommendations = []
        
        # 1. 弱点補強教材
        weak_subjects = self._find_weak_subjects(records)
        for subject in weak_subjects[:2]:
            suitable = self._find_materials_for_subject(
                subject, student.age_group, difficulty="easy"
            )
            for mat in suitable[:1]:
                recommendations.append({
                    "material": mat,
                    "reason": f"「{subject.value}」の基礎固めにおすすめ",
                    "priority": "high"
                })
        
        # 2. 得意分野を伸ばす教材
        strong_subjects = self._find_strong_subjects(records)
        for subject in strong_subjects[:1]:
            suitable = self._find_materials_for_subject(
                subject, student.age_group, difficulty="challenging"
            )
            for mat in suitable[:1]:
                recommendations.append({
                    "material": mat,
                    "reason": f"「{subject.value}」をさらに伸ばそう！",
                    "priority": "medium"
                })
        
        # 3. バランス良く学習するための教材
        untouched_subjects = self._find_untouched_subjects(records, student.age_group)
        for subject in untouched_subjects[:2]:
            suitable = self._find_materials_for_subject(
                subject, student.age_group
            )
            for mat in suitable[:1]:
                recommendations.append({
                    "material": mat,
                    "reason": f"新しい分野「{subject.value}」に挑戦してみよう！",
                    "priority": "medium"
                })
        
        return recommendations[:max_recommendations]
    
    def _recommend_by_age(
        self,
        student: Student,
        max_count: int
    ) -> List[Dict]:
        """年齢に基づく基本推薦"""
        suitable = [
            m for m in self.materials
            if m.age_group == student.age_group and m.difficulty <= 2
        ]
        
        return [
            {
                "material": mat,
                "reason": "はじめての学習におすすめ！",
                "priority": "high"
            }
            for mat in suitable[:max_count]
        ]
    
    def _find_weak_subjects(self, records: List[LearningRecord]) -> List[Subject]:
        """弱点科目を特定"""
        subject_scores = defaultdict(list)
        for r in records:
            subject_scores[r.subject].append(r.score)
        
        subject_averages = [
            (subject, statistics.mean(scores))
            for subject, scores in subject_scores.items()
        ]
        
        # スコアが低い順にソート
        subject_averages.sort(key=lambda x: x[1])
        
        return [s for s, _ in subject_averages if _ < 60][:3]
    
    def _find_strong_subjects(self, records: List[LearningRecord]) -> List[Subject]:
        """得意科目を特定"""
        subject_scores = defaultdict(list)
        for r in records:
            subject_scores[r.subject].append(r.score)
        
        subject_averages = [
            (subject, statistics.mean(scores))
            for subject, scores in subject_scores.items()
        ]
        
        # スコアが高い順にソート
        subject_averages.sort(key=lambda x: x[1], reverse=True)
        
        return [s for s, avg in subject_averages if avg > 75][:2]
    
    def _find_untouched_subjects(
        self,
        records: List[LearningRecord],
        age_group: AgeGroup
    ) -> List[Subject]:
        """未学習の科目を特定"""
        learned_subjects = {r.subject for r in records}
        
        # 年齢に応じた科目リスト
        if age_group == AgeGroup.INFANT:
            available = [Subject.JAPANESE, Subject.MATH, Subject.ART, Subject.MUSIC]
        else:
            available = list(Subject)
        
        return [s for s in available if s not in learned_subjects]
    
    def _find_materials_for_subject(
        self,
        subject: Subject,
        age_group: AgeGroup,
        difficulty: str = "normal"
    ) -> List[LearningMaterial]:
        """科目に適した教材を検索"""
        suitable = [
            m for m in self.materials
            if m.subject == subject and m.age_group == age_group
        ]
        
        if difficulty == "easy":
            suitable = [m for m in suitable if m.difficulty <= 2]
        elif difficulty == "challenging":
            suitable = [m for m in suitable if m.difficulty >= 3]
        
        return suitable
    
    def get_trending_materials(self, age_group: Optional[AgeGroup] = None) -> List[Dict]:
        """人気の教材を取得（デモ用）"""
        if age_group:
            filtered = [m for m in self.materials if m.age_group == age_group]
        else:
            filtered = self.materials
        
        # 実際のシステムでは使用頻度や評価でランキング
        return [
            {
                "material": mat,
                "popularity_score": 90 - (mat.difficulty * 10),
                "user_rating": 4.5 - (mat.difficulty * 0.2)
            }
            for mat in filtered[:5]
        ]
    
    def get_skill_based_recommendations(
        self,
        target_skills: List[SkillCategory],
        age_group: AgeGroup
    ) -> List[LearningMaterial]:
        """スキルベースの教材推薦"""
        matching = []
        
        for material in self.materials:
            if material.age_group != age_group:
                continue
            
            skill_match = len(set(material.skills) & set(target_skills))
            if skill_match > 0:
                matching.append((material, skill_match))
        
        # マッチ度が高い順にソート
        matching.sort(key=lambda x: x[1], reverse=True)
        
        return [m for m, _ in matching[:5]]
