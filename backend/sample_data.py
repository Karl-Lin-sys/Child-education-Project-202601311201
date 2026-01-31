"""
サンプル教育データ生成モジュール
デモンストレーション用のテストデータを生成
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict
from models import (
    Student, LearningRecord, LearningMaterial,
    AgeGroup, Subject, SkillCategory
)


# 日本の一般的な名前
FIRST_NAMES = [
    "ゆうと", "はると", "そうた", "ゆい", "めい", "あおい",
    "こはる", "ひなた", "れん", "みなと", "さくら", "あかり",
    "たくみ", "けいた", "りこ", "ほのか", "かいと", "ゆうき"
]


def generate_students(count: int = 30) -> List[Student]:
    """サンプル児童データを生成"""
    students = []
    for i in range(count):
        age = random.randint(3, 12)
        if age <= 5:
            age_group = AgeGroup.INFANT
            grade = None
        elif age <= 8:
            age_group = AgeGroup.LOWER_ELEMENTARY
            grade = age - 5
        else:
            age_group = AgeGroup.UPPER_ELEMENTARY
            grade = age - 5
        
        student = Student(
            id=f"STU{i+1:04d}",
            name=random.choice(FIRST_NAMES),
            age=age,
            age_group=age_group,
            grade=grade,
            enrollment_date=datetime.now() - timedelta(days=random.randint(30, 365))
        )
        students.append(student)
    return students


def generate_learning_records(
    students: List[Student],
    days: int = 90
) -> List[LearningRecord]:
    """学習記録を生成"""
    records = []
    record_id = 1
    
    for student in students:
        # 年齢に応じた科目を選択
        if student.age_group == AgeGroup.INFANT:
            subjects = [Subject.JAPANESE, Subject.MATH, Subject.ART, Subject.MUSIC]
        else:
            subjects = list(Subject)
        
        for day_offset in range(days):
            # 1日に1-3科目を学習
            daily_subjects = random.sample(subjects, min(len(subjects), random.randint(1, 3)))
            
            for subject in daily_subjects:
                # 基本スコアに個人差と成長を加味
                base_score = 50 + random.gauss(0, 15)
                growth_factor = day_offset * 0.1  # 時間経過で成長
                score = max(0, min(100, base_score + growth_factor + random.gauss(0, 10)))
                
                skill_scores = {}
                for skill in SkillCategory:
                    skill_scores[skill.value] = max(0, min(100, 
                        50 + random.gauss(0, 20) + growth_factor
                    ))
                
                record = LearningRecord(
                    id=f"REC{record_id:06d}",
                    student_id=student.id,
                    subject=subject,
                    score=round(score, 1),
                    duration_minutes=random.randint(15, 60),
                    date=datetime.now() - timedelta(days=days - day_offset),
                    skill_scores=skill_scores
                )
                records.append(record)
                record_id += 1
    
    return records


def generate_materials() -> List[LearningMaterial]:
    """教材データを生成"""
    materials = []
    material_id = 1
    
    material_templates = [
        ("ひらがなカード", Subject.JAPANESE, AgeGroup.INFANT, 1, 
         [SkillCategory.READING], "楽しくひらがなを覚えよう！", 15),
        ("かずあそび", Subject.MATH, AgeGroup.INFANT, 1,
         [SkillCategory.CALCULATION], "1から10までの数を学ぼう", 20),
        ("おえかきタイム", Subject.ART, AgeGroup.INFANT, 1,
         [SkillCategory.CREATIVITY], "自由に絵を描いてみよう", 30),
        ("読解ドリル初級", Subject.JAPANESE, AgeGroup.LOWER_ELEMENTARY, 2,
         [SkillCategory.READING, SkillCategory.LOGICAL_THINKING], "物語を読んで質問に答えよう", 25),
        ("計算マスター", Subject.MATH, AgeGroup.LOWER_ELEMENTARY, 2,
         [SkillCategory.CALCULATION], "足し算・引き算をマスターしよう", 20),
        ("理科実験キット", Subject.SCIENCE, AgeGroup.LOWER_ELEMENTARY, 2,
         [SkillCategory.LOGICAL_THINKING, SkillCategory.CREATIVITY], "身近な科学を体験しよう", 45),
        ("作文チャレンジ", Subject.JAPANESE, AgeGroup.UPPER_ELEMENTARY, 3,
         [SkillCategory.WRITING, SkillCategory.CREATIVITY], "テーマに沿って文章を書こう", 40),
        ("算数オリンピック", Subject.MATH, AgeGroup.UPPER_ELEMENTARY, 4,
         [SkillCategory.CALCULATION, SkillCategory.LOGICAL_THINKING], "難問に挑戦！", 50),
        ("英語スピーキング", Subject.ENGLISH, AgeGroup.UPPER_ELEMENTARY, 3,
         [SkillCategory.COMMUNICATION], "英語で自己紹介してみよう", 30),
        ("歴史探検", Subject.SOCIAL, AgeGroup.UPPER_ELEMENTARY, 3,
         [SkillCategory.READING, SkillCategory.LOGICAL_THINKING], "日本の歴史を学ぼう", 35),
    ]
    
    for template in material_templates:
        material = LearningMaterial(
            id=f"MAT{material_id:04d}",
            title=template[0],
            subject=template[1],
            age_group=template[2],
            difficulty=template[3],
            skills=template[4],
            description=template[5],
            duration_estimate=template[6]
        )
        materials.append(material)
        material_id += 1
    
    return materials


def get_sample_data() -> Dict:
    """全サンプルデータを取得"""
    students = generate_students(30)
    records = generate_learning_records(students, 90)
    materials = generate_materials()
    
    return {
        "students": students,
        "learning_records": records,
        "materials": materials
    }


if __name__ == "__main__":
    data = get_sample_data()
    print(f"生成された児童数: {len(data['students'])}")
    print(f"生成された学習記録数: {len(data['learning_records'])}")
    print(f"生成された教材数: {len(data['materials'])}")
