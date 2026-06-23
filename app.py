import streamlit as st

# ==========================================
# 1. 고정 데이터 및 규정 설정
# ==========================================
# 국수영 교과군 판별용
kme_subjects = [
    '독서 토론과 글쓰기', '인공지능 수학', '세계 문화와 영어', '언어생활 탐구', '기하', '경제 수학', 
    '미디어 영어', '문학과 영상', '미적분Ⅱ', '수학과제 탐구', '주제 탐구 독서', '매체 의사소통', 
    '수학과 문화', '실용 통계', '심화 영어', '영미 문학 읽기'
]

# 중복 편성 과목 (1회만 선택 가능)
overlap_list = [
    '지식 재산 일반', '기후변화와 환경생태', '융합과학 탐구', '생활과학 탐구', 
    '로봇과 공학세계', '생태와 환경', '인간과 심리', '교육의 이해', '인간과 경제활동'
]

# 위계성 규칙 (진로/융합 : 필수 선수 일반과목)
hierarchy_rules = {
    '역학과 에너지': '물리학', '전자기와 양자': '물리학',
    '화학 반응의 세계': '화학', '물질과 에너지': '화학',
    '생물의 유전': '생명과학', '세포와 물질대사': '생명과학',
    '지구시스템과학': '지구과학', '행성우주과학': '지구과학',
    '중국어 회화': '중국어', '심화 중국어': '중국어',
    '일본어 회화': '일본어', '심화 일본어': '일본어'
}

# ==========================================
# 2. 화면 구성 및 데이터 입력
# ==========================================
st.set_page_config(page_title="2026학년도 수강신청 검증", layout="wide")

st.title("📋 2026학년도 입학생 수강신청 사전 검증")
st.caption("안내문의 표와 동일하게 구성되어 있습니다. 각 학기별 정해진 과목 수에 맞게 체크해 주세요.")

# 학번/성명 입력
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.text_input("학번 (예: 10101)", key="st_id")
with col_info2:
    st.text_input("성명", key="st_name")

st.divider()

# 선택된 과목들을 담을 리스트와 그룹별 카운트 딕셔너리
selected_subjects = []
group_counts = {}

def create_checkbox_group(group_id, limit, subjects):
    count = 0
    # 화면을 2열 또는 3열로 나누어 체크박스 배치 (깔끔하게 보이기 위함)
    cols = st.columns(2)
    for idx, (subj, type_tag) in enumerate(subjects):
        with cols[idx % 2]:
            if st.checkbox(f"[{type_tag}] {subj}", key=f"{group_id}_{subj}"):
                selected_subjects.append(subj)
                count += 1
    group_counts[group_id] = {'count': count, 'limit': limit}

# --- 2학년 ---
st.header("📘 2학년 선택 과목")
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("2학년 1학기")
        st.write("📌 **[택 5]** 3학점 × 5과목 선택")
        create_checkbox_group("2-1-B", 5, [
            ('독서 토론과 글쓰기', '진로'), ('인공지능 수학', '진로'), ('세계 문화와 영어', '융합'), 
            ('현대사회와 윤리', '일반'), ('세계시민과 지리', '일반'), ('정치', '일반'), 
            ('동아시아 역사 기행', '진로'), ('물리학', '일반'), ('화학', '일반'), ('생명과학', '일반'), 
            ('기술·가정', '일반'), ('지식 재산 일반', '융합'), ('정보', '일반'), ('일본어', '일반'), ('중국어', '일반'), ('한문', '일반')
        ])
        st.divider()
        st.write("📌 **[택 1]** 예술 2학점 선택")
        create_checkbox_group("2-1-A", 1, [('음악 연주와 창작', '진로'), ('미술 창작', '진로')])

with col2:
    with st.container(border=True):
        st.subheader("2학년 2학기")
        st.write("📌 **[택 5]** 3학점 × 5과목 선택")
        create_checkbox_group("2-2-D", 5, [
            ('언어생활 탐구', '융합'), ('기하', '진로'), ('경제 수학', '진로'), ('미디어 영어', '융합'), 
            ('세계사', '일반'), ('인문학과 윤리', '융합'), ('법과 사회', '일반'), ('경제', '일반'), 
            ('한국지리 탐구', '진로'), ('지구과학', '일반'), ('역학과 에너지', '진로'), ('화학 반응의 세계', '진로'), 
            ('생물의 유전', '진로'), ('생활과학 탐구', '융합'), ('로봇과 공학세계', '진로'), ('인공지능 기초', '진로'), 
            ('일본어 회화', '진로'), ('중국어 회화', '진로')
        ])
        st.divider()
        st.write("📌 **[택 1]** 예술 2학점 선택")
        create_checkbox_group("2-2-C", 1, [('음악과 미디어', '융합'), ('미술과 매체', '융합')])

st.divider()

# --- 3학년 ---
st.header("📙 3학년 선택 과목")
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("3학년 1학기")
        st.write("📌 **[택 5]** 3학점 × 5과목 선택")
        create_checkbox_group("3-1-E", 5, [
            ('문학과 영상', '융합'), ('미적분Ⅱ', '진로'), ('수학과제 탐구', '진로'), ('사회와 문화', '일반'), 
            ('윤리와 사상', '일반'), ('물질과 에너지', '진로'), ('전자기와 양자', '진로'), ('세포와 물질대사', '진로'), 
            ('지구시스템과학', '진로'), ('행성우주과학', '진로'), ('융합과학 탐구', '융합'), ('생활과학 탐구', '융합'), 
            ('로봇과 공학세계', '진로'), ('데이터 과학', '진로'), ('심화 일본어', '진로'), ('심화 중국어', '진로')
        ])
        st.divider()
        st.write("📌 **[택 1]** 교양 2학점 선택")
        create_checkbox_group("3-1-F", 1, [('보건', '교양'), ('인간과 철학', '교양'), ('생태와 환경', '교양'), ('미술 감상과 비평', '교양')])

with col4:
    with st.container(border=True):
        st.subheader("3학년 2학기")
        st.write("📌 **[택 8]** 3학점 × 8과목 선택")
        create_checkbox_group("3-2-G", 8, [
            ('주제 탐구 독서', '진로'), ('매체 의사소통', '진로'), ('수학과 문화', '융합'), ('실용 통계', '융합'), 
            ('심화 영어', '진로'), ('영미 문학 읽기', '진로'), ('기후변화와 지속가능한 세계', '융합'), 
            ('역사로 탐구하는 현대 세계', '진로'), ('여행지리', '진로'), ('윤리문제 탐구', '진로'), 
            ('사회문제 탐구', '진로'), ('기후변화와 환경생태', '융합'), ('과학의 역사와 문화', '융합'), 
            ('융합과학 탐구', '융합'), ('아동발달과 부모', '융합'), ('지식 재산 일반', '융합'), 
            ('소프트웨어와 생활', '융합'), ('일본 문화', '융합'), ('운동과 건강', '일반'), ('음악 감상과 비평', '진로')
        ])
        st.divider()
        st.write("📌 **[택 1]** 교양/실무 2학점 선택")
        create_checkbox_group("3-2-H", 1, [('인간과 심리', '교양'), ('교육의 이해', '교양'), ('인간과 경제활동', '교양'), ('논리와 사고', '교양'), ('생애 설계와 자립', '교양')])

# ==========================================
# 3. 검증 로직 및 결과 출력
# ==========================================
st.divider()

if st.button("🔍 수강신청 규정 검증하기", use_container_width=True):
    if not st.session_state.st_id or not st.session_state.st_name:
        st.error("⚠️ 학번과 성명을 먼저 입력해 주세요.")
    else:
        errors = []
        
        # 1. 학기별 필수 선택 개수 검증
        group_names = {
            "2-1-B": "2학년 1학기 [택 5]", "2-1-A": "2학년 1학기 예술 [택 1]",
            "2-2-D": "2학년 2학기 [택 5]", "2-2-C": "2학년 2학기 예술 [택 1]",
            "3-1-E": "3학년 1학기 [택 5]", "3-1-F": "3학년 1학기 교양 [택 1]",
            "3-2-G": "3학년 2학기 [택 8]", "3-2-H": "3학년 2학기 교양 [택 1]"
        }
        for g_id, data in group_counts.items():
            if data['count'] != data['limit']:
                errors.append(f"🚩 **선택 개수 오류**: {group_names[g_id]} 영역에서 정확히 {data['limit']}과목을 선택해야 합니다. (현재 {data['count']}과목 선택됨)")
        
        # 2. 위계 검증
        for subj in selected_subjects:
            if subj in hierarchy_rules:
                pre_subj = hierarchy_rules[subj]
                if pre_subj not in selected_subjects:
                    errors.append(f"🚩 **위계 오류**: '{subj}'을(를) 수강하려면 1학기 또는 2학년에 선수 과목인 '{pre_subj}'을(를) 반드시 선택해야 합니다.")
        
        # 3. 국수영 8과목 제한 검증
        kme_count = len([s for s in selected_subjects if s in kme_subjects])
        if kme_count > 8:
            errors.append(f"🚩 **국/수/영 제한**: 선택한 국·수·영 과목이 {kme_count}개입니다. 최대 8개(24학점)까지만 선택 가능합니다.")

        # 4. 중복 수강 검증
        for overlap_subj in overlap_list:
            if selected_subjects.count(overlap_subj) > 1:
                errors.append(f"🚩 **중복 수강**: '{overlap_subj}' 과목을 2회 이상 체크했습니다. 3년간 1회만 수강 가능합니다.")

        # 결과 출력
        st.subheader(f"📊 {st.session_state.st_id} {st.session_state.st_name} 학생 검증 결과")
        if not errors:
            st.success("✅ 완벽합니다! 학기별 선택 개수, 졸업 요건, 과목 위계가 모두 정상입니다. 이대로 수강신청을 진행하세요.")
            st.balloons()
        else:
            st.error(f"❌ 총 {len(errors)}건의 오류가 발견되었습니다. 위로 올라가서 체크를 수정해 주세요.")
            for e in errors:
                st.warning(e)
