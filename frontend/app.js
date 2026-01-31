/**
 * メインアプリケーション - 教育研究プラットフォーム
 */
const API_BASE = 'http://localhost:5000/api';

// ページ切り替え
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const section = e.currentTarget.dataset.section;
        switchSection(section);
    });
});

function switchSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    document.getElementById(sectionId)?.classList.add('active');
    document.querySelector(`[data-section="${sectionId}"]`)?.classList.add('active');

    const titles = {
        dashboard: ['ダッシュボード', 'クラス全体の学習状況を確認できます'],
        students: ['児童一覧', '登録されている児童の一覧です'],
        analysis: ['学習分析', '個別児童の学習状況を分析します'],
        materials: ['教材', '利用可能な教材一覧です'],
        recommendations: ['AI推薦', 'AIによる教材推薦を確認できます']
    };

    document.getElementById('pageTitle').textContent = titles[sectionId]?.[0] || '';
    document.getElementById('pageDescription').textContent = titles[sectionId]?.[1] || '';
}

// API呼び出し
async function fetchAPI(endpoint) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`);
        return await res.json();
    } catch (e) {
        console.error('API Error:', e);
        return null;
    }
}

// ダッシュボード読み込み
async function loadDashboard() {
    const stats = await fetchAPI('/statistics');
    if (stats) {
        document.getElementById('totalStudents').textContent = stats.total_students || 0;
        document.getElementById('totalRecords').textContent = stats.total_records || 0;
        document.getElementById('overallAverage').textContent = stats.overall_average ? stats.overall_average.toFixed(1) : '-';

        if (stats.subject_averages) renderSubjectChart(stats.subject_averages);
        if (stats.age_group_statistics) renderAgeGroupChart(stats.age_group_statistics);
    }

    const materials = await fetchAPI('/materials');
    document.getElementById('totalMaterials').textContent = materials?.total || 0;

    loadRecentActivity();
}

async function loadRecentActivity() {
    const data = await fetchAPI('/learning-records?limit=10');
    const container = document.getElementById('recentActivity');

    if (!data?.records?.length) {
        container.innerHTML = '<div class="loading">データがありません</div>';
        return;
    }

    container.innerHTML = data.records.map(r => {
        const scoreClass = r.score >= 80 ? 'high' : r.score >= 60 ? 'medium' : 'low';
        return `
            <div class="activity-item">
                <div class="activity-icon">📝</div>
                <div class="activity-info">
                    <span class="name">${r.student_id}</span>
                    <span class="details">${r.subject} - ${r.duration_minutes}分</span>
                </div>
                <span class="activity-score ${scoreClass}">${r.score.toFixed(0)}点</span>
            </div>
        `;
    }).join('');
}

// 児童一覧
async function loadStudents() {
    const data = await fetchAPI('/students');
    const grid = document.getElementById('studentsGrid');

    if (!data?.students?.length) {
        grid.innerHTML = '<div class="loading">児童データがありません</div>';
        return;
    }

    grid.innerHTML = data.students.map(s => {
        const ageClass = s.age_group === '幼児' ? 'infant' : s.age_group === '低学年' ? 'lower' : 'upper';
        return `
            <div class="student-card" onclick="selectStudent('${s.id}')">
                <div class="student-header">
                    <div class="student-avatar">👦</div>
                    <div>
                        <div class="student-name">${s.name}</div>
                        <div class="student-age">${s.age}歳</div>
                    </div>
                </div>
                <div class="student-details">
                    <span class="student-tag age-${ageClass}">${s.age_group}</span>
                    ${s.grade ? `<span class="student-tag">${s.grade}年生</span>` : ''}
                </div>
            </div>
        `;
    }).join('');

    populateStudentSelects(data.students);
}

function populateStudentSelects(students) {
    const options = students.map(s => `<option value="${s.id}">${s.name} (${s.age}歳)</option>`).join('');
    document.getElementById('analysisStudentSelect').innerHTML = '<option value="">-- 選択してください --</option>' + options;
    document.getElementById('recommendationStudentSelect').innerHTML = '<option value="">-- 選択してください --</option>' + options;
}

function selectStudent(id) {
    document.getElementById('analysisStudentSelect').value = id;
    switchSection('analysis');
    loadAnalysis(id);
}

// 学習分析
document.getElementById('analysisStudentSelect')?.addEventListener('change', (e) => {
    if (e.target.value) loadAnalysis(e.target.value);
});

async function loadAnalysis(studentId) {
    const container = document.getElementById('analysisContent');
    container.innerHTML = '<div class="loading">分析中...</div>';

    const data = await fetchAPI(`/students/${studentId}/analysis`);
    if (!data) {
        container.innerHTML = '<div class="placeholder-message"><p>分析データがありません</p></div>';
        return;
    }

    const patterns = data.learning_patterns || {};
    container.innerHTML = `
        <div class="analysis-section">
            <h4>📊 学習パターン</h4>
            <div class="patterns-grid">
                <div class="pattern-item">
                    <div class="pattern-label">総学習時間</div>
                    <div class="pattern-value">${patterns.total_study_minutes || 0}分</div>
                </div>
                <div class="pattern-item">
                    <div class="pattern-label">平均セッション</div>
                    <div class="pattern-value">${patterns.average_session_minutes || 0}分</div>
                </div>
                <div class="pattern-item">
                    <div class="pattern-label">集中力指数</div>
                    <div class="pattern-value">${patterns.focus_index || 0}</div>
                </div>
                <div class="pattern-item">
                    <div class="pattern-label">総セッション数</div>
                    <div class="pattern-value">${patterns.total_sessions || 0}回</div>
                </div>
            </div>
        </div>
        <div class="analysis-section">
            <h4>💪 強み</h4>
            <div class="skill-list">
                ${(data.strengths || []).map(s => `<span class="skill-tag strength">${s}</span>`).join('') || 'データ不足'}
            </div>
        </div>
        <div class="analysis-section">
            <h4>📈 改善ポイント</h4>
            <div class="skill-list">
                ${(data.areas_for_improvement || []).map(s => `<span class="skill-tag improvement">${s}</span>`).join('') || 'なし'}
            </div>
        </div>
        <div class="analysis-section">
            <h4>💡 アドバイス</h4>
            <div class="tips-list">
                ${(data.personalized_tips || []).map(t => `<div class="tip-item">${t}</div>`).join('') || 'なし'}
            </div>
        </div>
    `;
}

// 教材一覧
document.getElementById('materialsAgeFilter')?.addEventListener('change', loadMaterials);

async function loadMaterials() {
    const filter = document.getElementById('materialsAgeFilter').value;
    const endpoint = filter ? `/materials?age_group=${encodeURIComponent(filter)}` : '/materials';
    const data = await fetchAPI(endpoint);
    const grid = document.getElementById('materialsGrid');

    if (!data?.materials?.length) {
        grid.innerHTML = '<div class="loading">教材がありません</div>';
        return;
    }

    grid.innerHTML = data.materials.map(m => `
        <div class="material-card">
            <div class="material-header">
                <span class="material-title">${m.title}</span>
                <span class="material-subject">${m.subject}</span>
            </div>
            <p class="material-description">${m.description}</p>
            <div class="material-meta">
                <span>🎯 ${m.age_group}</span>
                <span class="difficulty-stars">${'★'.repeat(m.difficulty)}${'☆'.repeat(5 - m.difficulty)}</span>
                <span>⏱️ ${m.duration_estimate}分</span>
            </div>
        </div>
    `).join('');
}

// AI推薦
document.getElementById('recommendationStudentSelect')?.addEventListener('change', (e) => {
    if (e.target.value) loadRecommendations(e.target.value);
});

async function loadRecommendations(studentId) {
    const container = document.getElementById('recommendationsContent');
    container.innerHTML = '<div class="loading">推薦を生成中...</div>';

    const data = await fetchAPI(`/students/${studentId}/recommendations`);
    if (!data?.recommendations?.length) {
        container.innerHTML = '<div class="placeholder-message"><p>推薦データがありません</p></div>';
        return;
    }

    container.innerHTML = data.recommendations.map(r => `
        <div class="recommendation-card">
            <div class="recommendation-priority ${r.priority}">📕</div>
            <div class="recommendation-content">
                <div class="recommendation-title">${r.material.title}</div>
                <div class="recommendation-reason">${r.reason}</div>
                <div class="recommendation-meta">
                    <span>🎯 ${r.material.age_group}</span>
                    <span>📚 ${r.material.subject}</span>
                    <span>⏱️ ${r.material.duration_estimate}分</span>
                </div>
            </div>
        </div>
    `).join('');
}

// ヘルスチェック
async function checkAPIHealth() {
    const status = document.getElementById('apiStatus');
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            status.className = 'api-status connected';
            status.innerHTML = '<span class="status-dot"></span><span>API接続中</span>';
        } else throw new Error();
    } catch {
        status.className = 'api-status error';
        status.innerHTML = '<span class="status-dot"></span><span>API未接続</span>';
    }
}

// 更新ボタン
document.getElementById('refreshBtn')?.addEventListener('click', () => {
    loadDashboard();
    loadStudents();
    loadMaterials();
});

// 初期化
checkAPIHealth();
loadDashboard();
loadStudents();
loadMaterials();
