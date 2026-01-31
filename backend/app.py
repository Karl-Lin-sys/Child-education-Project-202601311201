"""
小学・幼児教育研究プラットフォーム
Flask API サーバー
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from dataclasses import asdict
from datetime import datetime

from models import Subject, SkillCategory, AgeGroup
from sample_data import get_sample_data
from analyzer import LearningAnalyzer
from recommender import MaterialRecommender

app = Flask(__name__)
CORS(app)

# サンプルデータを初期化
data = get_sample_data()
analyzer = LearningAnalyzer(data["students"], data["learning_records"])
recommender = MaterialRecommender(
    data["students"],
    data["learning_records"],
    data["materials"]
)


def serialize_datetime(obj):
    """日時オブジェクトをシリアライズ"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def serialize_enum(obj):
    """Enumオブジェクトをシリアライズ"""
    if hasattr(obj, 'value'):
        return obj.value
    return obj


def serialize_dataclass(obj):
    """データクラスを辞書に変換"""
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            result[field] = serialize_value(value)
        return result
    return obj


def serialize_value(value):
    """値を再帰的にシリアライズ"""
    if isinstance(value, datetime):
        return value.isoformat()
    elif hasattr(value, 'value'):  # Enum
        return value.value
    elif hasattr(value, '__dataclass_fields__'):
        return serialize_dataclass(value)
    elif isinstance(value, list):
        return [serialize_value(v) for v in value]
    elif isinstance(value, dict):
        return {k: serialize_value(v) for k, v in value.items()}
    return value


@app.route('/api/health', methods=['GET'])
def health_check():
    """ヘルスチェック"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@app.route('/api/students', methods=['GET'])
def get_students():
    """全児童リストを取得"""
    students_data = []
    for student in data["students"]:
        students_data.append(serialize_dataclass(student))
    return jsonify({"students": students_data, "total": len(students_data)})


@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """個別児童情報を取得"""
    for student in data["students"]:
        if student.id == student_id:
            return jsonify(serialize_dataclass(student))
    return jsonify({"error": "Student not found"}), 404


@app.route('/api/students/<student_id>/analysis', methods=['GET'])
def get_student_analysis(student_id):
    """児童の学習分析を取得"""
    result = analyzer.analyze_student(student_id)
    if result is None:
        return jsonify({"error": "Analysis not available"}), 404
    return jsonify(serialize_dataclass(result))


@app.route('/api/students/<student_id>/recommendations', methods=['GET'])
def get_student_recommendations(student_id):
    """児童への教材推薦を取得"""
    recommendations = recommender.recommend_for_student(student_id)
    
    serialized = []
    for rec in recommendations:
        serialized.append({
            "material": serialize_dataclass(rec["material"]),
            "reason": rec["reason"],
            "priority": rec["priority"]
        })
    
    return jsonify({"recommendations": serialized})


@app.route('/api/statistics', methods=['GET'])
def get_class_statistics():
    """クラス全体の統計を取得"""
    stats = analyzer.get_class_statistics()
    return jsonify(stats)


@app.route('/api/materials', methods=['GET'])
def get_materials():
    """教材一覧を取得"""
    age_group_param = request.args.get('age_group')
    
    materials_data = []
    for material in data["materials"]:
        if age_group_param:
            if material.age_group.value != age_group_param:
                continue
        materials_data.append(serialize_dataclass(material))
    
    return jsonify({"materials": materials_data, "total": len(materials_data)})


@app.route('/api/materials/trending', methods=['GET'])
def get_trending_materials():
    """人気教材を取得"""
    age_group_param = request.args.get('age_group')
    
    age_group = None
    if age_group_param:
        for ag in AgeGroup:
            if ag.value == age_group_param:
                age_group = ag
                break
    
    trending = recommender.get_trending_materials(age_group)
    
    serialized = []
    for item in trending:
        serialized.append({
            "material": serialize_dataclass(item["material"]),
            "popularity_score": item["popularity_score"],
            "user_rating": item["user_rating"]
        })
    
    return jsonify({"trending": serialized})


@app.route('/api/learning-records', methods=['GET'])
def get_learning_records():
    """学習記録を取得"""
    student_id = request.args.get('student_id')
    limit = request.args.get('limit', 100, type=int)
    
    records = data["learning_records"]
    
    if student_id:
        records = [r for r in records if r.student_id == student_id]
    
    records = records[:limit]
    
    serialized = [serialize_dataclass(r) for r in records]
    return jsonify({"records": serialized, "total": len(serialized)})


@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """科目一覧を取得"""
    subjects = [{"id": s.name, "name": s.value} for s in Subject]
    return jsonify({"subjects": subjects})


@app.route('/api/skills', methods=['GET'])
def get_skills():
    """スキルカテゴリ一覧を取得"""
    skills = [{"id": s.name, "name": s.value} for s in SkillCategory]
    return jsonify({"skills": skills})


@app.route('/api/age-groups', methods=['GET'])
def get_age_groups():
    """年齢グループ一覧を取得"""
    age_groups = [{"id": ag.name, "name": ag.value} for ag in AgeGroup]
    return jsonify({"age_groups": age_groups})


if __name__ == '__main__':
    print("=" * 50)
    print("小学・幼児教育研究プラットフォーム")
    print("Child Education Research Platform")
    print("=" * 50)
    print(f"サンプルデータ:")
    print(f"  - 児童数: {len(data['students'])}")
    print(f"  - 学習記録数: {len(data['learning_records'])}")
    print(f"  - 教材数: {len(data['materials'])}")
    print("=" * 50)
    print("Starting server at http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
