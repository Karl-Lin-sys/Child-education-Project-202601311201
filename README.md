# 小学・幼児教育研究プラットフォーム
# Child Education Research Platform

AIを活用した児童の学習分析・進捗追跡・教材推薦システム

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📚 概要

小学生および幼児（3〜12歳）の教育効果を分析・研究するためのWebプラットフォームです。

### 主な機能

- **📊 学習データ分析**: 児童の学習パターン、成績推移、スキル発達を分析
- **📈 進捗追跡**: 科目別・スキル別の成長を可視化
- **💡 AI教材推薦**: 個々の学習状況に基づいた最適な教材を推薦
- **🎨 ダッシュボード**: 保護者・教育者向けのインタラクティブなレポート

## 🏗️ プロジェクト構造

```
child_education_project/
├── backend/
│   ├── app.py              # Flask API サーバー
│   ├── analyzer.py         # 学習分析モジュール
│   ├── recommender.py      # AI推薦エンジン
│   ├── models.py           # データモデル定義
│   └── sample_data.py      # サンプルデータ生成
├── frontend/
│   ├── index.html          # ダッシュボード
│   ├── styles.css          # スタイルシート
│   ├── app.js              # アプリケーションロジック
│   └── charts.js           # チャート描画
├── README.md
└── requirements.txt
```

## 🚀 セットアップ

### 必要環境
- Python 3.8以上
- pip

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/I-PingLin/Child-education-Project-202601311201.git
cd Child-education-Project-202601311201

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 起動方法

```bash
# バックエンドサーバーを起動
cd backend
python app.py
```

サーバーが起動したら、ブラウザで `frontend/index.html` を開いてダッシュボードを表示します。

## 📊 API エンドポイント

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/api/health` | GET | ヘルスチェック |
| `/api/students` | GET | 児童一覧取得 |
| `/api/students/<id>` | GET | 個別児童情報 |
| `/api/students/<id>/analysis` | GET | 学習分析結果 |
| `/api/students/<id>/recommendations` | GET | AI教材推薦 |
| `/api/statistics` | GET | クラス統計 |
| `/api/materials` | GET | 教材一覧 |
| `/api/learning-records` | GET | 学習記録 |

## 🧠 技術スタック

### バックエンド
- **Flask**: RESTful API フレームワーク
- **Python**: データ分析・機械学習

### フロントエンド
- **HTML5/CSS3**: モダンUI
- **JavaScript**: インタラクティブ機能
- **Chart.js**: データ可視化

## 📖 機能詳細

### 学習分析 (analyzer.py)
- 科目別成績分析
- 週別成績推移トラッキング
- 集中力指数計算
- 強み・改善点の自動特定
- パーソナライズされた学習アドバイス生成

### AI推薦エンジン (recommender.py)
- 弱点補強教材の推薦
- 得意分野を伸ばす教材の提案
- 未学習分野への挑戦促進
- スキルベースのマッチング

## 🎯 対象年齢層

| 分類 | 年齢 | 対応科目 |
|-----|-----|---------|
| 幼児 | 3-5歳 | 国語、算数、図工、音楽 |
| 低学年 | 6-8歳 | 全科目 |
| 高学年 | 9-12歳 | 全科目 |

## 📝 ライセンス

MIT License

## 👨‍💻 作者

I-Ping Lin

---

*このプロジェクトは教育研究を目的として開発されました。*
