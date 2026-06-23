import streamlit as st

# ==========================================
# 1. 과목 및 위계 데이터 설정
# ==========================================
# 과학 및 제2외국어 위계성 데이터 (진로/융합 선택 : 필수 선수 일반 선택)
hierarchy_rules = {
    '역학과 에너지': '물리학',
    '전자기와 양자': '물리학',
    '화학반응의세계': '화학',
    '물질과 에너지': '화학',
    '생물의 유전': '생명과학',
    '세포와 물질대사': '생명과학',
    '지구시스템과학': '지구과학',
    '행성우주과학': '지구과학',
    '중국어 회화': '중국어',
    '심화 중국어': '중국어',
    '일본어 회화': '일본어',
    '심화 일본어': '일본어'
}

# 중복 편성 과목 (1회만 선택 가능)
overlapping_subjects = [
    '지식재산일반', '기후변화와환경생태', '융합과학탐구', '생활과학탐구', 
    '로봇과공학세계', '생태와환경', '인간과심리', '교육의이해', '인간과경제활동'
]

# UI를 위한 가상의 과목 리스트 (실제 학교 편제표에 맞게 수정하여 사용)
kme_list = ['문학', '독서와 작문', '화법과 언어', '미적분Ⅰ', '확률과 통계', '영어 회화', '영미 문학 읽기'] + [f'국수영 가상과목{i}' for i in range(1, 5)]
tech_info_foreign_list = ['기술·가정', '정보', '중국어', '일본어', '중국어 회화', '심화 중국어', '일본어 회화', '심화 일본어']
liberal_arts_list = ['논리학', '심리학', '교육학', '철학']
arts_list = ['음악 감상과 비평', '미술 창작', '미술 감상과 비평'] # 2학년 예술 선택
science_list = ['물리학', '화학', '생명과학', '지구과학', '역학과 에너지', '전자기와 양자', '화학반응의세계', '물질과 에너지', '생물의 유전', '세포와 물질대사', '지구시스템과학', '행성우주과학']


# ==========================================
# 2. 웹 UI 화면 구성
# ==========================================
st.set_page_config(page_title="수강신청 사전 검증", layout="centered")
st.title("🎓 2학년 수강신청 사전 검증 프로그램")
st.info("본인이 신청할 과목들을 모두 선택한 후, 하단의 [검증하기] 버튼을 눌러주세요.")

st.subheader("1. 국어/수학/영어 교과군 (최대 8과목)")
selected_kme = st.multiselect("국/수/영 과목을 선택하세요 (최대 8과목 제한)", kme_list)

st.subheader("2. 기술·가정/정보/제2외국어/한문/교양 교과군")
st.markdown("* 교양은 학기별 1과목씩 총 2과목(4학점) 필수\n* 나머지 교과군에서 3학점짜리 4과목(12학점) 필수 선택")
selected_liberal = st.multiselect("교양 과목을 선택하세요 (2과목 필수)", liberal_arts_list)
selected_tif = st.multiselect("기/가/정보/제2외국어 과목을 선택하세요 (4과목 필수)", tech_info_foreign_list)

st.subheader("3. 과학 탐구 교과군 (위계 확인 필수)")
selected_science = st.multiselect("과학 과목을 선택하세요", science_list)

st.subheader("4. 중복 편성 과목 (1회만 선택 가능)")
selected_overlap = st.multiselect("중복 편성된 과목을 선택하세요", overlapping_subjects)

st.subheader("5. 예술 교과군 (4학점 필수)")
selected_arts = st.multiselect("예술 과목을 선택하세요 (본교 기준 4학점 충족 필요)", arts_list)

# 모든 선택 과목 통합
all_selected = selected_kme + selected_liberal + selected_tif + selected_science + selected_overlap + selected_arts


# ==========================================
# 3. 검증 로직 실행
# ==========================================
st.divider()
if st.button("🚀 시간표 검증하기", use_container_width=True):
    errors = []
    
    # [규칙 1] 국/수/영 8과목(24학점) 초과 금지
    if len(selected_kme) > 8:
        errors.append(f"국/수/영 과목을 8과목 초과하여 선택했습니다. (현재 {len(selected_kme)}과목)")
        
    # [규칙 2] 중복 편성 과목 1회 제한 (multiselect에서는 기본적으로 중복 선택이 안 되지만, 방어적 로직 추가)
    if len(selected_overlap) != len(set(selected_overlap)):
        errors.append("중복 편성된 과목을 2회 이상 선택했습니다.")
        
    # [규칙 3] 기술·가정/정보/제2외국어/교양 16학점 검증
    if len(selected_liberal) != 2:
        errors.append(f"교양 과목은 2과목(4학점)을 선택해야 합니다. (현재 {len(selected_liberal)}과목)")
    if len(selected_tif) < 4:
        errors.append(f"기술·가정/정보/제2외국어 교과군에서 최소 4과목(12학점) 이상 선택해야 합니다. (현재 {len(selected_tif)}과목)")
        
    # [규칙 4] 과학 및 제2외국어 위계성 검증
    for subject in all_selected:
        if subject in hierarchy_rules:
            required_subject = hierarchy_rules[subject]
            # 선수 과목을 선택하지 않은 경우 오류
            if required_subject not in all_selected:
                errors.append(f"위계 오류: '{subject}' 수강을 위해 선수 과목인 '{required_subject}'(을)를 함께 선택해야 합니다.")
                
    # [규칙 5] 예술 교과 4학점 검증 (보통 1과목이 2학점 단위로 운영되어 2과목 선택 시 4학점 충족이라 가정)
    if len(selected_arts) < 2:  
        errors.append("예술 교과군에서 4학점(예: 2학점짜리 2과목)을 충족하도록 선택해야 합니다.")

    # ==========================================
    # 4. 결과 출력
    # ==========================================
    if not errors:
        st.success("✅ 축하합니다! 모든 졸업 요건과 위계 규정에 맞게 수강신청이 완료되었습니다. 이대로 최종 제출을 진행해 주세요.")
        st.balloons()
    else:
        st.error("❌ 수강신청 내역에 아래와 같은 오류가 있습니다. 수정 후 다시 검증해 주세요.")
        for i, error_msg in enumerate(errors, 1):
            st.warning(f"{i}. {error_msg}")
