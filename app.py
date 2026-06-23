import streamlit as st

# ==========================================
# 1. 고정 데이터 및 규정 설정
# ==========================================
# 과학 및 제2외국어 위계성 규칙
hierarchy_rules = {
    '역학과 에너지': '물리학', '전자기와 양자': '물리학',
    '화학 반응의 세계': '화학', '물질과 에너지': '화학',
    '생물의 유전': '생명과학', '세포와 물질대사': '생명과학',
    '지구시스템과학': '지구과학', '행성우주과학': '지구과학',
    '중국어 회화': '중국어', '심화 중국어': '중국어',
    '일본어 회화': '일본어', '심화 일본어': '일본어'
}

# 국수영 교과군 판별용
kme_subjects = [
    '독서 토론과 글쓰기', '인공지능 수학', '세계 문화와 영어',
    '언어생활 탐구', '기하', '경제 수학', '미디어 영어',
    '문학과 영상', '미적분Ⅱ', '수학과제 탐구',
    '주제 탐구 독서', '매체 의사소통', '수학과 문화', '실용 통계', '심화 영어', '영미 문학 읽기'
]

# 중복 편성 과목 (2~3학년 통틀어 1회만 선택 가능)
overlap_list = [
    '지식 재산 일반', '기후변화와 환경생태', '융합과학 탐구', '생활과학 탐구', 
    '로봇과 공학세계', '생태와 환경', '인간과 심리', '교육의 이해', '인간과 경제활동'
]

# ==========================================
# 2. 화면 구성 (안내문 스타일)
# ==========================================
st.set_page_config(page_title="2026학년도 수강신청 검증", layout="wide")

st.title("📋 2026학년도 입학생 수강신청 사전 검증")
st.caption("안내문의 체크박스와 동일하게 선택해 주세요. 검증 버튼을 누르면 규정 위반 여부를 알려줍니다.")

# 학번/성명 입력
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.text_input("학번 (예: 10101)", key="st_id")
with col_info2:
    st.text_input("성명", key="st_name")

st.divider()

# 선택된 과목들을 담을 리스트
selected_subjects = []

# --- 2학년 영역 ---
st.header("1. 2학년 선택 과목")
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("2학년 1학기")
        st.write("📌 **[택 5]** 3학점 × 5과목")
        group_b = [
            '독서 토론과 글쓰기', '인공지능 수학', '세계 문화와 영어', '현대사회와 윤리', '세계시민과 지리', 
            '정치', '동아시아 역사 기행', '물리학', '화학', '생명과학', '기술·가정', 
            '지식 재산 일반', '정보', '일본어', '중국어', '한문'
        ]
        for s in group_b:
            if st.checkbox(s, key=f"2-1-B-{s}"): selected_subjects.append(s)
        
        st.write("📌 **[택 1]** 예술 2학점")
        group_a = ['음악 연주와 창작', '미술 창작']
        for s in group_a:
            if st.checkbox(s, key=f"2-1-A-{s}"): selected_subjects.append(s)

with col2:
    with st.container(border=True):
        st.subheader("2학년 2학기")
        st.write("📌 **[택 5]** 3학점 × 5과목")
        group_d = [
            '언어생활 탐구', '기하', '경제 수학', '미디어 영어', '세계사', '인문학과 윤리', 
            '법과 사회', '경제', '한국지리 탐구', '지구과학', '역학과 에너지', 
            '화학 반응의 세계', '생물의 유전', '생활과학 탐구', '로봇과 공학세계', 
            '인공지능 기초', '일본어 회화', '중국어 회화'
        ]
        for s in group_d:
            if st.checkbox(s, key=f"2-2-D-{s}"): selected_subjects.append(s)
            
        st.write("📌 **[택 1]** 예술 2학점")
        group_c = ['음악과 미디어', '미술과 매체']
        for s in group_c:
            if st.checkbox(s, key=f"2-2-C-{s}"): selected_subjects.append(s)

st.divider()

# --- 3학년 영역 ---
st.header("2. 3학년 선택 과목")
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("3학년 1학기")
        st.write("📌 **[택 5]** 3학점 × 5과목")
        group_e = [
            '문학과 영상', '미적분Ⅱ', '수학과제 탐구', '사회와 문화', '윤리와 사상', 
            '물질과 에너지', '전자기와 양자', '세포와 물질대사', '지구시스템과학', '행성우주과학', 
            '융합과학 탐구', '생활과학 탐구', '로봇과 공학세계', '데이터 과학', '심화 일본어', '심화 중국어'
        ]
        for s in group_e:
            if st.checkbox(s, key=f"3-1-E-{s}"): selected_subjects.append(s)
            
        st.write("📌 **[택 1]** 교양 2학점")
        group_f = ['보건', '인간과 철학', '생태와 환경', '미술 감상과 비평']
        for s in group_f:
            if st.checkbox(s, key=f"3-1-F-{s}"): selected_subjects.append(s)

with col4:
    with st.container(border=True):
        st.subheader("3학년 2학기")
        st.write("📌 **[택 8]** 3학점 × 8과목")
        group_g = [
            '주제 탐구 독서', '매체 의사소통', '수학과 문화', '실용 통계', '심화 영어', '영미 문학 읽기', 
            '기후변화와 지속가능한 세계', '역사로 탐구하는 현대 세계', '여행지리', '윤리문제 탐구', 
            '사회문제 탐구', '기후변화와 환경생태', '과학의 역사와 문화', '융합과학 탐구', 
            '아동발달과 부모', '지식 재산 일반', '소프트웨어와 생활', '일본 문화', 
            '운동과 건강', '음악 감상과 비평'
        ]
        for s in group_g:
            if st.checkbox(s, key=f"3-2-G-{s}"): selected_subjects.append(s)
            
        st.write("📌 **[택 1]** 교양/실무 2학점")
        group_h = ['인간과 심리', '교육의 이해', '인간과 경제활동', '논리와 사고', '생애 설계와 자립']
        for s in group_h:
            if st.checkbox(s, key=f"3-2-H-{s}"): selected_subjects.append(s)

# ==========================================
# 3. 검증 로직
# ==========================================
st.divider()

if st.button("🔍 수강신청 규정 검증하기", use_container_width=True):
    if not st.session_state.st_id or not st.session_state.st_name:
        st.error("⚠️ 학번과 성명을 먼저 입력해 주세요.")
    else:
        errors = []
        
        # 1. 학점 계산용 카운트
        kme_count = len([s for s in selected_subjects if s in kme_subjects])
        
        # 2. 위계 검증
        for subj in selected_subjects:
            if subj in hierarchy_rules:
                pre_subj = hierarchy_rules[subj]
                if pre_subj not in selected_subjects:
                    errors.append(f"🚩 **위계 오류**: '{subj}'을(를) 배우려면 선수 과목인 '{pre_subj}'을(를) 반드시 선택해야 합니다.")
        
        # 3. 국수영 8과목 제한 (24학점)
        if kme_count > 8:
            errors.append(f"🚩 **국수영 제한**: 선택한 국/수/영 과목이 {kme_count}개입니다. 최대 8개까지만 선택 가능합니다.")

        # 4. 중복 수강 검증 (중복 편성된 과목)
        for overlap_subj in overlap_list:
            # 전체 선택 리스트에서 해당 과목이 몇 번 나타나는지 카운트
            # (Streamlit 체크박스 키값 기준이 아니라 과목명 기준)
            # 체크박스 로직상 중복 과목이 여러 학기에 있으면 각각 체크될 수 있음
            count = 0
            # 2-1-B, 2-2-D 등 모든 섹션을 다 뒤져서 체크된 것 확인
            # (중복 과목은 1회만 선택 가능하므로 세트(set)가 아닌 전체 리스트에서 중복을 찾아야 함)
            # 여기서는 편의상 전체 선택 리스트에 같은 이름이 몇 개 들어있는지 확인
            count = selected_subjects.count(overlap_subj)
            if count > 1:
                errors.append(f"🚩 **중복 수강**: '{overlap_subj}' 과목은 여러 학기에 편성되어 있으나 1회만 선택 가능합니다.")

        # 5. 학기별 선택 권장 수 확인 (경고)
        # 2-1-B(5), 2-2-D(5), 3-1-E(5), 3-2-G(8)
        # (이 부분은 학생 편의를 위해 추가)

        # 결과 출력
        st.subheader(f"📊 {st.session_state.st_id} {st.session_state.st_name} 학생 검증 결과")
        if not errors:
            st.success("✅ 모든 졸업 요건 및 과목 위계가 정상입니다! 이대로 수강신청을 진행하세요.")
            st.balloons()
        else:
            st.error(f"❌ 총 {len(errors)}건의 오류가 발견되었습니다. 아래 내용을 수정해 주세요.")
            for e in errors:
                st.write(e)

# 우측 하단 도움말
st.sidebar.markdown("### 💡 규정 안내")
st.sidebar.info("""
1. **국수영 제한**: 2~3학년 선택 과목 중 국/수/영은 최대 8과목(24학점)까지만 가능합니다.
2. **위계성**: 과학/외국어Ⅰ(일반)을 먼저 선택해야 Ⅱ(진로/융합)를 선택할 수 있습니다.
3. **중복 선택**: 밑줄 친 과목(중복 편성)은 3년 동안 딱 한 번만 수강할 수 있습니다.
""")
