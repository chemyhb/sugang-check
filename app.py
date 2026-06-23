import streamlit as st
import pandas as pd

# ==========================================
# 1. 고정 데이터 및 규정 설정
# ==========================================
kme_subjects = [
    '독서 토론과 글쓰기', '인공지능 수학', '세계 문화와 영어', '언어생활 탐구', '미디어 영어', '기하', '경제 수학', 
    '영어 독해와 작문', '문학과 영상', '수학과제 탐구', '미적분Ⅱ', 
    '영미 문학 읽기', '주제 탐구 독서', '심화 영어', '매체 의사소통', '실용 통계', '수학과 문화'
]

tech_info_foreign_subjects = [
    '기술·가정', '정보', '일본어', '중국어', '한문', '지식 재산 일반', 
    '로봇과 공학세계', '생활과학 탐구', '인공지능 기초', '일본어 회화', '중국어 회화', 
    '데이터 과학', '심화 일본어', '심화 중국어', '아동발달과 부모', '소프트웨어와 생활', '일본 문화'
]

overlap_list = [
    '지식 재산 일반', '기후변화와 환경생태', '융합과학 탐구', '생활과학 탐구', 
    '로봇과 공학세계', '생태와 환경', '인간과 심리', '교육의 이해', '인간과 경제활동'
]

hierarchy_rules = {
    '역학과 에너지': '물리학', '전자기와 양자': '물리학',
    '화학 반응의 세계': '화학', '물질과 에너지': '화학',
    '생물의 유전': '생명과학', '세포와 물질대사': '생명과학',
    '지구시스템과학': '지구과학', '행성우주과학': '지구과학',
    '중국어 회화': '중국어', '심화 중국어': '중국어',
    '일본어 회화': '일본어', '심화 일본어': '일본어'
}

# 리로스쿨 화면과 동일한 그룹 및 제한 인원
groups_info = {
    "2-1 [택5]": {"limit": 5, "semester": "2학년 1학기"},
    "2-1 예술 [택1]": {"limit": 1, "semester": "2학년 1학기"},
    "2-2 [택5]": {"limit": 5, "semester": "2학년 2학기"},
    "2-2 예술 [택1]": {"limit": 1, "semester": "2학년 2학기"},
    "3-1 [택5]": {"limit": 5, "semester": "3학년 1학기"},
    "3-1 교양 [택1]": {"limit": 1, "semester": "3학년 1학기"},
    "3-2 [택8]": {"limit": 8, "semester": "3학년 2학기"},
    "3-2 교양 [택1]": {"limit": 1, "semester": "3학년 2학기"}
}

# 과목 데이터 (UI를 위해 리스트 형태로 재구성)
subject_list = {
    "2-1 [택5]": [
        ('독서 토론과 글쓰기', '융합', '국어'), ('인공지능 수학', '진로', '수학'), ('세계 문화와 영어', '융합', '영어'),
        ('현대사회와 윤리', '일반', '사회'), ('정치', '진로', '사회'), ('세계시민과 지리', '일반', '사회'), ('동아시아 역사 기행', '진로', '사회'), ('금융과 경제생활', '융합', '사회'),
        ('물리학', '일반', '과학'), ('화학', '일반', '과학'), ('생명과학', '일반', '과학'), ('기후변화와 환경생태', '융합', '과학'),
        ('기술·가정', '일반', '기가/제2'), ('정보', '일반', '기가/제2'), ('일본어', '일반', '기가/제2'), ('중국어', '일반', '기가/제2'), ('지식 재산 일반', '융합', '기가/제2'), ('한문', '일반', '기가/제2')
    ],
    "2-1 예술 [택1]": [('음악 연주와 창작', '진로', '예술'), ('미술 창작', '진로', '예술')],
    "2-2 [택5]": [
        ('언어생활 탐구', '융합', '국어'), ('기하', '진로', '수학'), ('경제 수학', '진로', '수학'), ('미디어 영어', '융합', '영어'),
        ('인문학과 윤리', '진로', '사회'), ('세계사', '일반', '사회'), ('한국지리 탐구', '진로', '사회'), ('법과 사회', '진로', '사회'), ('경제', '진로', '사회'),
        ('지구과학', '일반', '과학'), ('역학과 에너지', '진로', '과학'), ('화학 반응의 세계', '진로', '과학'), ('생물의 유전', '진로', '과학'), ('융합과학 탐구', '융합', '과학'),
        ('로봇과 공학세계', '진로', '기가/제2'), ('생활과학 탐구', '진로', '기가/제2'), ('인공지능 기초', '진로', '기가/제2'), ('일본어 회화', '진로', '기가/제2'), ('중국어 회화', '진로', '기가/제2')
    ],
    "2-2 예술 [택1]": [('음악과 미디어', '융합', '예술'), ('미술과 매체', '융합', '예술')],
    "3-1 [택5]": [
        ('문학과 영상', '진로', '국어'), ('수학과제 탐구', '융합', '수학'), ('미적분Ⅱ', '진로', '수학'), ('영어 독해와 작문', '일반', '영어'),
        ('사회와 문화', '일반', '사회'), ('윤리와 사상', '진로', '사회'), ('기후변화와 지속가능한 세계', '융합', '사회'),
        ('물질과 에너지', '진로', '과학'), ('세포와 물질대사', '진로', '과학'), ('지구시스템과학', '진로', '과학'), ('전자기와 양자', '진로', '과학'), ('행성우주과학', '진로', '과학'), ('융합과학 탐구', '융합', '과학'),
        ('생활과학 탐구', '진로', '기가/제2'), ('로봇과 공학세계', '진로', '기가/제2'), ('데이터 과학', '진로', '기가/제2'), ('심화 일본어', '진로', '기가/제2'), ('심화 중국어', '진로', '기가/제2'),
        ('미술 감상과 비평', '진로', '예술')
    ],
    "3-1 교양 [택1]": [('인간과 철학', '진로', '교양'), ('보건', '진로', '교양'), ('생태와 환경', '일반', '교양'), ('인간과 심리', '진로', '교양'), ('교육의 이해', '진로', '교양'), ('인간과 경제활동', '융합', '교양')],
    "3-2 [택8]": [
        ('주제 탐구 독서', '진로', '국어'), ('매체 의사소통', '융합', '국어'), ('실용 통계', '융합', '수학'), ('수학과 문화', '융합', '수학'), ('영미 문학 읽기', '진로', '영어'), ('심화 영어', '진로', '영어'),
        ('여행지리', '융합', '사회'), ('사회문제 탐구', '융합', '사회'), ('윤리문제 탐구', '융합', '사회'), ('역사로 탐구하는 현대 세계', '융합', '사회'),
        ('과학의 역사와 문화', '융합', '과학'), ('기후변화와 환경생태', '융합', '과학'), ('융합과학 탐구', '융합', '과학'),
        ('지식 재산 일반', '융합', '기가/제2'), ('아동발달과 부모', '융합', '기가/제2'), ('소프트웨어와 생활', '융합', '기가/제2'), ('일본 문화', '융합', '기가/제2'),
        ('운동과 건강', '일반', '체육'), ('음악 감상과 비평', '진로', '예술')
    ],
    "3-2 교양 [택1]": [('논리와 사고', '진로', '교양'), ('생애 설계와 자립', '융합', '교양'), ('생태와 환경', '일반', '교양'), ('인간과 심리', '진로', '교양'), ('교육의 이해', '진로', '교양'), ('인간과 경제활동', '융합', '교양')]
}

@st.dialog("🔔 수강신청 검증 결과")
def show_result_dialog(errors):
    if errors:
        st.error(f"❌ 총 {len(errors)}건의 오류가 발견되었습니다. 확인 후 과목 선택을 수정해 주세요.")
        for e in errors:
            st.warning(e)
    else:
        st.success("✅ 완벽합니다! 모든 졸업 필수 요건과 과목 위계 규정을 충족했습니다.")
        st.balloons()
        st.info("이대로 실제 수강신청 시스템에 입력하시면 됩니다.")

# ==========================================
# 3. 화면 UI (리로스쿨 스타일)
# ==========================================
st.set_page_config(page_title="2026 수강신청 검증", layout="wide")
st.title("📚 2026학년도 수강신청 사전 검증")
st.caption("실제 수강신청 화면과 유사하게 구성되었습니다. 아래에서 과목을 선택하면 상단의 [본인 선택 과목]에 실시간으로 반영됩니다.")

# 상단: 학생 정보
col_info1, col_info2, col_empty = st.columns([1, 1, 3])
with col_info1:
    st_id = st.text_input("학번", placeholder="예: 10101")
with col_info2:
    st_name = st.text_input("성명")

st.divider()

# Session State 초기화 (체크박스 상태 저장을 위함)
for group in groups_info.keys():
    if f"selected_{group}" not in st.session_state:
        st.session_state[f"selected_{group}"] = []

# ==========================================
# [본인 선택 과목] (상단 고정 요약표)
# ==========================================
st.subheader("📋 본인 선택 과목")
st.write("실시간으로 담은 과목을 확인하세요.")

# 학기별로 컬럼을 나누어 표 형태로 출력
sum_cols = st.columns(4)
col_idx = 0

for sem in ["2학년 1학기", "2학년 2학기", "3학년 1학기", "3학년 2학기"]:
    with sum_cols[col_idx]:
        st.markdown(f"**{sem}**")
        # 해당 학기에 속하는 그룹들의 선택 과목을 모두 모음
        sem_subjects = []
        for g_name, g_info in groups_info.items():
            if g_info["semester"] == sem:
                sem_subjects.extend(st.session_state[f"selected_{g_name}"])
        
        if sem_subjects:
            df_display = pd.DataFrame(sem_subjects, columns=["선택 과목"])
            st.dataframe(df_display, hide_index=True, use_container_width=True)
        else:
            st.caption("선택 내역 없음")
    col_idx += 1

st.divider()

# ==========================================
# [수요조사 과목 선택] (하단 리스트 폼)
# ==========================================
st.subheader("📝 과목 선택 (수요조사)")

# 리로스쿨처럼 화면을 가로로 분할하여 그룹별로 배치
tabs = st.tabs(list(groups_info.keys()))

for i, (group_name, info) in enumerate(groups_info.items()):
    with tabs[i]:
        st.markdown(f"#### {info['semester']} - {group_name.split(' ')[-1]}")
        st.write(f"최대 **{info['limit']}과목**을 선택해야 합니다. 굵은 글씨(🔄)는 중복 편성 과목입니다.")
        
        # 선택된 과목 수를 시각적으로 표시
        current_count = len(st.session_state[f"selected_{group_name}"])
        if current_count == info['limit']:
            st.success(f"✅ {current_count}/{info['limit']} 선택 완료")
        elif current_count > info['limit']:
            st.error(f"❌ {current_count}/{info['limit']} 초과 선택!")
        else:
            st.info(f"👉 {current_count}/{info['limit']} 선택 중")

        # 과목 리스트를 체크박스로 출력
        cols = st.columns(3) # 3열 배치로 깔끔하게
        for idx, (subj, tag, cat) in enumerate(subject_list[group_name]):
            with cols[idx % 3]:
                # 중복 과목 강조
                display_name = f"**{subj}** 🔄" if subj in overlap_list else subj
                
                # 체크박스 생성
                is_checked = subj in st.session_state[f"selected_{group_name}"]
                if st.checkbox(f"[{cat}-{tag}] {display_name}", value=is_checked, key=f"chk_{group_name}_{subj}"):
                    if subj not in st.session_state[f"selected_{group_name}"]:
                        st.session_state[f"selected_{group_name}"].append(subj)
                        st.rerun() # 실시간 반영을 위한 화면 새로고침
                else:
                    if subj in st.session_state[f"selected_{group_name}"]:
                        st.session_state[f"selected_{group_name}"].remove(subj)
                        st.rerun() # 실시간 반영을 위한 화면 새로고침

st.divider()

# ==========================================
# 4. 최종 검증 및 버튼 (제출)
# ==========================================
if st.button("🚀 최종 수강신청 검증하기", use_container_width=True, type="primary"):
    if not st_id or not st_name:
        st.error("⚠️ 상단에 학번과 성명을 먼저 입력해 주세요.")
    else:
        errors = []
        all_selected = []
        
        # 1. 개수 검증 및 전체 선택 과목 리스트 병합
        for g_name, info in groups_info.items():
            selected = st.session_state[f"selected_{g_name}"]
            all_selected.extend(selected)
            if len(selected) != info['limit']:
                errors.append(f"🚩 **선택 개수 오류**: [{g_name}] 영역에서 정확히 {info['limit']}과목을 선택해야 합니다. (현재 {len(selected)}개)")

        # 2. 위계 검증
        for subj in all_selected:
            if subj in hierarchy_rules:
                pre_subj = hierarchy_rules[subj]
                if pre_subj not in all_selected:
                    errors.append(f"🚩 **위계 오류**: '{subj}' 수강을 위해 1단계 선수 과목 '{pre_subj}'을(를) 함께 선택해야 합니다.")
        
        # 3. 국수영 8과목 제한 검증
        kme_count = len([s for s in all_selected if s in kme_subjects])
        if kme_count > 8:
            errors.append(f"🚩 **국/수/영 제한**: 국·수·영 과목이 {kme_count}개입니다. 최대 8과목(24학점)까지만 선택 가능합니다.")

        # 4. 중복 수강 검증
        for overlap_subj in overlap_list:
            if all_selected.count(overlap_subj) > 1:
                errors.append(f"🚩 **중복 수강**: '{overlap_subj}' 과목을 2회 이상 선택했습니다. 3년간 1회만 수강 가능합니다.")

        # 5. 기술·가정/정보/제2외국어/한문 필수 12학점 검증
        tif_count = len([s for s in all_selected if s in tech_info_foreign_subjects])
        if tif_count < 4:
            errors.append(f"🚩 **필수 이수 부족**: 기/가·정보·제2외국어·한문 교과군에서 최소 4과목 이상 선택해야 합니다. (현재 {tif_count}과목)")

        # 결과 팝업
        show_result_dialog(errors)
