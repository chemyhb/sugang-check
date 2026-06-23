import streamlit as st

# ==========================================
# 1. 고정 데이터 및 규정 설정
# ==========================================
# 국수영 교과군 판별용 (실제 편제표 기준 국, 수, 영 모든 선택과목)
kme_subjects = [
    '독서 토론과 글쓰기', '인공지능 수학', '세계 문화와 영어', 
    '언어생활 탐구', '미디어 영어', '기하', '경제 수학', 
    '영어 독해와 작문', '문학과 영상', '수학과제 탐구', '미적분Ⅱ', 
    '영미 문학 읽기', '주제 탐구 독서', '심화 영어', '매체 의사소통', '실용 통계', '수학과 문화'
]

# 중복 편성 과목 (1회만 선택 가능 - 선생님 제공 지침 기준)
overlap_list = [
    '지식 재산 일반', '기후변화와 환경생태', '융합과학 탐구', '생활과학 탐구', 
    '로봇과 공학세계', '생태와 환경', '인간과 심리', '교육의 이해', '인간과 경제활동'
]

# 위계성 규칙
hierarchy_rules = {
    '역학과 에너지': '물리학', '전자기와 양자': '물리학',
    '화학 반응의 세계': '화학', '물질과 에너지': '화학',
    '생물의 유전': '생명과학', '세포와 물질대사': '생명과학',
    '지구시스템과학': '지구과학', '행성우주과학': '지구과학',
    '중국어 회화': '중국어', '심화 중국어': '중국어',
    '일본어 회화': '일본어', '심화 일본어': '일본어'
}

# 학기 매핑 딕셔너리
semester_mapping = {
    "2-1-B": "2학년 1학기 [택 5]", "2-1-A": "2학년 1학기 예술 [택 1]",
    "2-2-D": "2학년 2학기 [택 5]", "2-2-C": "2학년 2학기 예술 [택 1]",
    "3-1-E": "3학년 1학기 [택 5]", "3-1-F": "3학년 1학기 교양 [택 1]",
    "3-2-G": "3학년 2학기 [택 8]", "3-2-H": "3학년 2학기 교양 [택 1]"
}

# ==========================================
# 2. 팝업창(Dialog) 함수 정의
# ==========================================
@st.dialog("🔔 수강신청 검증 결과")
def show_result_dialog(errors):
    if errors:
        st.error(f"❌ 총 {len(errors)}건의 오류가 발견되었습니다. 창을 닫고 수정해 주세요.")
        for e in errors:
            st.warning(e)
    else:
        st.success("✅ 완벽합니다! 학기별 선택 개수, 졸업 요건, 과목 위계가 모두 정상입니다.")
        st.balloons()
        st.info("창을 닫고 화면 맨 아래의 '수강신청 내역 요약'을 확인한 후 최종 제출해 주세요.")

# ==========================================
# 3. 화면 구성 및 데이터 입력
# ==========================================
st.set_page_config(page_title="2026학년도 수강신청 검증", layout="wide")

st.title("📋 2026학년도 입학생 수강신청 사전 검증")
st.caption("안내문의 표와 동일하게 구성되어 있습니다. 교과별 분류를 확인하고 학기별 정해진 과목 수에 맞게 체크해 주세요.")

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.text_input("학번 (예: 10101)", key="st_id")
with col_info2:
    st.text_input("성명", key="st_name")

st.divider()

selected_subjects = []
group_counts = {}

# 학기별 선택 과목을 저장할 딕셔너리
selected_by_semester = {
    "2학년 1학기 [택 5]": [], "2학년 1학기 예술 [택 1]": [],
    "2학년 2학기 [택 5]": [], "2학년 2학기 예술 [택 1]": [],
    "3학년 1학기 [택 5]": [], "3학년 1학기 교양 [택 1]": [],
    "3학년 2학기 [택 8]": [], "3학년 2학기 교양 [택 1]": []
}

def create_categorized_checkbox_group(group_id, limit, categorized_subjects):
    count = 0
    semester_name = semester_mapping[group_id]
    for category, subjects in categorized_subjects.items():
        st.markdown(f"**🔹 {category}**") 
        cols = st.columns(2)
        for idx, (subj, type_tag) in enumerate(subjects):
            with cols[idx % 2]:
                if st.checkbox(f"[{type_tag}] {subj}", key=f"{group_id}_{subj}"):
                    selected_subjects.append(subj)
                    selected_by_semester[semester_name].append(f"[{type_tag}] {subj}")
                    count += 1
    group_counts[group_id] = {'count': count, 'limit': limit}

# --- 2학년 ---
st.header("📘 2학년 선택 과목")
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("2학년 1학기")
        st.write("📌 **[택 5]** 3학점 × 5과목 선택")
        create_categorized_checkbox_group("2-1-B", 5, {
            "국어/수학/영어": [('독서 토론과 글쓰기', '융합'), ('인공지능 수학', '진로'), ('세계 문화와 영어', '융합')],
            "사회": [('현대사회와 윤리', '일반'), ('정치', '진로'), ('세계시민과 지리', '일반'), ('동아시아 역사 기행', '진로'), ('금융과 경제생활', '융합')],
            "과학": [('물리학', '일반'), ('화학', '일반'), ('생명과학', '일반'), ('기후변화와 환경생태', '융합')],
            "기술·가정 / 제2외국어 / 한문": [('기술·가정', '일반'), ('정보', '일반'), ('일본어', '일반'), ('중국어', '일반'), ('지식 재산 일반', '융합'), ('한문', '일반')]
        })
        st.divider()
        st.write("📌 **[택 1]** 예술 2학점 선택")
        create_categorized_checkbox_group("2-1-A", 1, {
            "예술": [('음악 연주와 창작', '진로'), ('미술 창작', '진로')]
        })

with col2:
    with st.container(border=True):
        st.subheader("2학년 2학기")
        st.write("📌 **[택 5]** 3학점 × 5과목 선택")
        create_categorized_checkbox_group("2-2-D", 5, {
            "국어/수학/영어": [('언어생활 탐구', '융합'), ('미디어 영어', '융합'), ('기하', '진로'), ('경제 수학', '진로')],
            "사회": [('인문학과 윤리', '진로'), ('세계사', '일반'), ('한국지리 탐구', '진로'), ('법과 사회', '진로'), ('경제', '진로')],
            "과학": [('지구과학', '일반'), ('역학과 에너지', '진로'), ('화학 반응의 세계', '진로'), ('생물의 유전', '진로'), ('융합과학 탐구', '융합')],
            "기술·가정 / 제2외국어 / 정보": [('로봇과 공학세계', '진로'), ('생활과학 탐구', '진로'), ('인공지능 기초', '진로'), ('일본어 회화', '진로'), ('중국어 회화', '진로')]
        })
        st.divider()
        st.write("📌 **[택 1]** 예술 2학점 선택")
        create_categorized_checkbox_group("2-2-C", 1, {
            "예술": [('음악과 미디어', '융합'), ('미술과 매체', '융합')]
        })

st.divider()

# --- 3학년 ---
st.header("📙 3학년 선택 과목")
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("3학년 1학기")
        st.write("📌 **[택 5]** 3학점 × 5과목 선택")
        create_categorized_checkbox_group("3-1-E", 5, {
            "국어/수학/영어": [('영어 독해와 작문', '일반'), ('문학과 영상', '진로'), ('수학과제 탐구', '융합'), ('미적분Ⅱ', '진로')],
            "사회 / 예술": [('사회와 문화', '일반'), ('미술 감상과 비평', '진로'), ('기후변화와 지속가능한 세계', '융합'), ('윤리와 사상', '진로')],
            "과학": [('물질과 에너지', '진로'), ('세포와 물질대사', '진로'), ('지구시스템과학', '진로'), ('전자기와 양자', '진로'), ('행성우주과학', '진로'), ('융합과학 탐구', '융합')],
            "기술·가정 / 제2외국어 / 정보": [('데이터 과학', '진로'), ('심화 일본어', '진로'), ('심화 중국어', '진로'), ('생활과학 탐구', '진로'), ('로봇과 공학세계', '진로')]
        })
        st.divider()
        st.write("📌 **[택 1]** 교양 2학점 선택")
        create_categorized_checkbox_group("3-1-F", 1, {
            "교양": [('인간과 철학', '진로'), ('보건', '진로')]
        })

with col4:
    with st.container(border=True):
        st.subheader("3학년 2학기")
        st.write("📌 **[택 8]** 3학점 × 8과목 선택")
        create_categorized_checkbox_group("3-2-G", 8, {
            "국어/수학/영어": [('영미 문학 읽기', '진로'), ('주제 탐구 독서', '진로'), ('심화 영어', '진로'), ('매체 의사소통', '융합'), ('실용 통계', '융합'), ('수학과 문화', '융합')],
            "사회 / 체육 / 예술": [('여행지리', '융합'), ('사회문제 탐구', '융합'), ('운동과 건강', '진로'), ('음악 감상과 비평', '진로'), ('윤리문제 탐구', '융합'), ('역사로 탐구하는 현대 세계', '융합')],
            "과학": [('과학의 역사와 문화', '융합'), ('기후변화와 환경생태', '융합')],
            "기술·가정 / 정보 / 제2외국어": [('지식 재산 일반', '융합'), ('아동발달과 부모', '융합'), ('소프트웨어와 생활', '융합'), ('일본 문화', '융합')]
        })
        st.divider()
        st.write("📌 **[택 1]** 교양/실무 2학점 선택")
        create_categorized_checkbox_group("3-2-H", 1, {
            "교양 / 기술·가정": [('생태와 환경', '일반'), ('인간과 심리', '진로'), ('교육의 이해', '진로'), ('인간과 경제활동', '융합'), ('논리와 사고', '진로'), ('생애 설계와 자립*', '융합')]
        })

# ==========================================
# 4. 검증 로직 및 결과 요약 출력
# ==========================================
st.divider()

if st.button("🔍 수강신청 규정 검증하기", use_container_width=True):
    if not st.session_state.st_id or not st.session_state.st_name:
        st.error("⚠️ 학번과 성명을 먼저 입력해 주세요.")
    else:
        errors = []
        
        # 1. 학기별 필수 선택 개수 검증
        for g_id, data in group_counts.items():
            if data['count'] != data['limit']:
                errors.append(f"🚩 **선택 개수 오류**: {semester_mapping[g_id]} 영역에서 정확히 {data['limit']}과목을 선택해야 합니다. (현재 {data['count']}과목 선택됨)")
        
        # 2. 위계 검증
        for subj in selected_subjects:
            if subj in hierarchy_rules:
                pre_subj = hierarchy_rules[subj]
                if pre_subj not in selected_subjects:
                    errors.append(f"🚩 **위계 오류**: '{subj}'을(를) 수강하려면 선수 과목인 '{pre_subj}'을(를) 반드시 함께 선택해야 합니다.")
        
        # 3. 국수영 8과목 제한 검증
        kme_count = len([s for s in selected_subjects if s in kme_subjects])
        if kme_count > 8:
            errors.append(f"🚩 **국/수/영 제한**: 선택한 국·수·영 과목이 {kme_count}개입니다. 최대 8개(24학점)까지만 선택 가능합니다.")

        # 4. 중복 수강 검증
        for overlap_subj in overlap_list:
            if selected_subjects.count(overlap_subj) > 1:
                errors.append(f"🚩 **중복 수강**: '{overlap_subj}' 과목을 2회 이상 체크했습니다. 3년간 1회만 수강 가능합니다.")

        # 팝업창 호출
        show_result_dialog(errors)
        
        # 화면 하단에 학기별 수강신청 내역 요약본 출력
        st.subheader(f"📋 {st.session_state.st_id} {st.session_state.st_name} 학생 수강신청 내역 요약")
        
        summary_cols = st.columns(4)
        col_idx = 0
        for sem, subjs in selected_by_semester.items():
            with summary_cols[col_idx % 4]:
                st.markdown(f"**{sem}**")
                if subjs:
                    for s in subjs:
                        st.write(f"- {s}")
                else:
                    st.caption("선택 과목 없음")
                st.write("") # 간격 띄우기
            col_idx += 1
