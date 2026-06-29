import streamlit as st; st.html("<style>footer {visibility: hidden;} .stAppDeployButton {display: none;} div[data-testid='stStatusWidget'] {display: none;}</style>")
import pandas as pd
import requests

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

mandatory_subjects = {
    "2학년 1학기": [("[일반]", "문학", 4), ("[일반]", "대수", 4), ("[일반]", "영어Ⅰ", 4), ("[융합]", "스포츠 생활1", 2)],
    "2학년 2학기": [("[일반]", "독서와 작문", 4), ("[일반]", "미적분Ⅰ", 4), ("[일반]", "영어Ⅱ", 4), ("[융합]", "스포츠 생활2", 2)],
    "3학년 1학기": [("[일반]", "화법과 언어", 4), ("[일반]", "확률과 통계", 4), ("[진로]", "스포츠 문화*", 2)],
    "3학년 2학기": [("[진로]", "스포츠 과학*", 1)]
}

groups_info = {
    "2-1 [택5]": {"limit": 5, "semester": "2학년 1학기", "title": "📌 3학점 × 5과목 선택", "credit": 3},
    "2-1 예술 [택1]": {"limit": 1, "semester": "2학년 1학기", "title": "📌 예술 2학점 × 1과목 선택", "credit": 2},
    "2-2 [택5]": {"limit": 5, "semester": "2학년 2학기", "title": "📌 3학점 × 5과목 선택", "credit": 3},
    "2-2 예술 [택1]": {"limit": 1, "semester": "2학년 2학기", "title": "📌 예술 2학점 × 1과목 선택", "credit": 2},
    "3-1 [택5]": {"limit": 5, "semester": "3학년 1학기", "title": "📌 3학점 × 5과목 선택", "credit": 3},
    "3-1 교양 [택1]": {"limit": 1, "semester": "3학년 1학기", "title": "📌 교양/예술 2학점 × 1과목 선택", "credit": 2},
    "3-2 [택8]": {"limit": 8, "semester": "3학년 2학기", "title": "📌 3학점 × 8과목 선택", "credit": 3},
    "3-2 교양 [택1]": {"limit": 1, "semester": "3학년 2학기", "title": "📌 교양 2학점 × 1과목 선택", "credit": 2}
}

subject_list = {
    "2-1 [택5]": [
        ('독서 토론과 글쓰기', '융합', '국어'), ('인공지능 수학', '진로', '수학'), ('세계 문화와 영어', '융합', '영어'),
        ('현대사회와 윤리', '일반', '사회'), ('정치', '진로', '사회'), ('세계시민과 지리', '일반', '사회'), ('동아시아 역사 기행', '진로', '사회'), ('금융과 경제생활', '융합', '사회'),
        ('물리학', '일반', '과학'), ('화학', '일반', '과학'), ('생명과학', '일반', '과학'), ('기후변화와 환경생태', '융합', '과학'),
        ('기술·가정', '일반', '기술·가정/정보/제2외국어'), ('정보', '일반', '기술·가정/정보/제2외국어'), ('일본어', '일반', '기술·가정/정보/제2외국어'), ('중국어', '일반', '기술·가정/정보/제2외국어'), ('지식 재산 일반', '융합', '기술·가정/정보/제2외국어'), ('한문', '일반', '기술·가정/정보/제2외국어')
    ],
    "2-1 예술 [택1]": [('음악 연주와 창작', '진로', '예술'), ('미술 창작', '진로', '예술')],
    "2-2 [택5]": [
        ('언어생활 탐구', '융합', '국어'), ('기하', '진로', '수학'), ('경제 수학', '진로', '수학'), ('미디어 영어', '융합', '영어'),
        ('인문학과 윤리', '진로', '사회'), ('세계사', '일반', '사회'), ('한국지리 탐구', '진로', '사회'), ('법과 사회', '진로', '사회'), ('경제', '진로', '사회'),
        ('지구과학', '일반', '과학'), ('역학과 에너지', '진로', '과학'), ('화학 반응의 세계', '진로', '과학'), ('생물의 유전', '진로', '과학'), ('융합과학 탐구', '융합', '과학'),
        ('로봇과 공학세계', '진로', '기술·가정/정보/제2외국어'), ('생활과학 탐구', '진로', '기술·가정/정보/제2외국어'), ('인공지능 기초', '진로', '기술·가정/정보/제2외국어'), ('일본어 회화', '진로', '기술·가정/정보/제2외국어'), ('중국어 회화', '진로', '기술·가정/정보/제2외국어')
    ],
    "2-2 예술 [택1]": [('음악과 미디어', '융합', '예술'), ('미술과 매체', '융합', '예술')],
    "3-1 [택5]": [
        ('문학과 영상', '진로', '국어'), ('수학과제 탐구', '융합', '수학'), ('미적분Ⅱ', '진로', '수학'), ('영어 독해와 작문', '일반', '영어'),
        ('사회와 문화', '일반', '사회'), ('윤리와 사상', '진로', '사회'), ('기후변화와 지속가능한 세계', '융합', '사회'),
        ('물질과 에너지', '진로', '과학'), ('세포와 물질대사', '진로', '과학'), ('지구시스템과학', '진로', '과학'), ('전자기와 양자', '진로', '과학'), ('행성우주과학', '진로', '과학'), ('융합과학 탐구', '융합', '과학'),
        ('생활과학 탐구', '진로', '기술·가정/정보/제2외국어'), ('로봇과 공학세계', '진로', '기술·가정/정보/제2외국어'), ('데이터 과학', '진로', '기술·가정/정보/제2외국어'), ('심화 일본어', '진로', '기술·가정/정보/제2외국어'), ('심화 중국어', '진로', '기술·가정/정보/제2외국어'),
        ('미술 감상과 비평', '진로', '예술')
    ],
    "3-1 교양 [택1]": [('인간과 철학', '진로', '교양'), ('보건', '진로', '교양'), ('생태와 환경', '일반', '교양'), ('인간과 심리', '진로', '교양'), ('교육의 이해', '진로', '교양'), ('인간과 경제활동', '융합', '교양')],
    "3-2 [택8]": [
        ('주제 탐구 독서', '진로', '국어'), ('매체 의사소통', '융합', '국어'), ('실용 통계', '융합', '수학'), ('수학과 문화', '융합', '수학'), ('영미 문학 읽기', '진로', '영어'), ('심화 영어', '진로', '영어'),
        ('여행지리', '융합', '사회'), ('사회문제 탐구', '융합', '사회'), ('윤리문제 탐구', '융합', '사회'), ('역사로 탐구하는 현대 세계', '융합', '사회'),
        ('과학의 역사와 문화', '융합', '과학'), ('기후변화와 환경생태', '융합', '과학'), ('융합과학 탐구', '융합', '과학'),
        ('지식 재산 일반', '융합', '기술·가정/정보/제2외국어'), ('아동발달과 부모', '융합', '기술·가정/정보/제2외국어'), ('소프트웨어와 생활', '융합', '기술·가정/정보/제2외국어'), ('일본 문화', '융합', '기술·가정/정보/제2외국어'),
        ('운동과 건강', '일반', '체육'), ('음악 감상과 비평', '진로', '예술')
    ],
    "3-2 교양 [택1]": [('논리와 사고', '진로', '교양'), ('생애 설계와 자립', '융합', '교양'), ('생태와 환경', '일반', '교양'), ('인간과 심리', '진로', '교양'), ('교육의 이해', '진로', '교양'), ('인간과 경제활동', '융합', '교양')]
}

@st.dialog("🔔 수강신청 조건 확인 결과")
def show_error_dialog(errors):
    st.error(f"❌ 총 {len(errors)}건의 안내 사항이 있습니다. 아래 내용을 확인하여 과목을 조정해 주세요.")
    for e in errors:
        st.warning(e)

# ==========================================
# Session State 및 함수
# ==========================================
semester_tabs = ["2학년 1학기", "2학년 2학기", "3학년 1학기", "3학년 2학기"]

if 'current_sem_idx' not in st.session_state:
    st.session_state.current_sem_idx = 0
if 'is_valid' not in st.session_state:
    st.session_state.is_valid = False

def set_tab(idx):
    st.session_state.current_sem_idx = idx

def go_next():
    if st.session_state.current_sem_idx < len(semester_tabs) - 1:
        st.session_state.current_sem_idx += 1

def go_prev():
    if st.session_state.current_sem_idx > 0:
        st.session_state.current_sem_idx -= 1

# ==========================================
# 3. 화면 UI 
# ==========================================
st.set_page_config(page_title="성덕고 수강신청 사전 진단", layout="wide")
st.title("📚성덕고 2026학년도 입학생 수강신청 사전 진단 시스템")
st.caption("각 학기 탭에서 과목을 모두 선택한 후, 하단의 [조건 확인] 버튼을 눌러 통과하면 데이터를 제출할 수 있습니다.")

col_class, col_num, col_name, col_empty = st.columns([1, 1, 2, 2])
with col_class:
    st_class = st.selectbox("반", [f"{i}반" for i in range(1, 12)]) 
with col_num:
    st_num = st.selectbox("번호", [f"{i}번" for i in range(1, 31)]) 
with col_name:
    st_name = st.text_input("성명", placeholder="예: 홍길동")

st.divider()

with st.expander("🚨 **[필독] 수강신청 시 반드시 확인해야 할 5가지 필수 조건 (클릭해서 확인)**", expanded=True):
    st.markdown("""
    1. **선수 과목(위계) 조건 확인**: 과학 및 제2외국어 교과의 심화 과목(진로/융합)을 들으려면, 반드시 해당 과목의 기초 과목(일반)을 함께 선택해야 합니다. *(예: '생물의 유전' 선택 시 '생명과학' 필수)*
    2. **국·수·영 균형 이수**: 다양한 교과 학습을 위해 국어, 수학, 영어 교과군에 속하는 선택 과목은 3년 동안 **최대 8과목(24학점)까지만** 선택할 수 있습니다.
    3. **필수 교과 영역 이수**: 기술·가정, 정보, 제2외국어, 한문 교과군 안에서 3년 동안 **최소 4과목(12학점) 이상**을 반드시 선택해야 합니다.
    4. **중복 편성 과목 1회 수강**: 과목명 옆에 **(중복)** 표시가 있는 과목은 여러 학기에 걸쳐 개설되어 있지만, **3년 동안 딱 한 학기에서만** 골라야 합니다.
    5. **학기별 정해진 과목 수 준수**: 각 학기별로 [택 5], [택 1] 등 정해진 필수 선택 개수를 정확히 맞춰야 합니다.
    """)

st.divider()

for group in groups_info.keys():
    if f"selected_{group}" not in st.session_state:
        st.session_state[f"selected_{group}"] = []

# ==========================================
# [수강신청 과목 선택 영역]
# ==========================================
st.subheader("📝 과목 선택")

tab_cols = st.columns(len(semester_tabs))
for i, sem in enumerate(semester_tabs):
    with tab_cols[i]:
        btn_type = "primary" if st.session_state.current_sem_idx == i else "secondary"
        st.button(sem, key=f"tab_btn_{i}", type=btn_type, use_container_width=True, on_click=set_tab, args=(i,))

current_sem = semester_tabs[st.session_state.current_sem_idx]
st.markdown(f"### ➡️ {current_sem}")

cat_order_list = ['국어', '수학', '영어', '사회', '과학', '기술·가정/정보/제2외국어', '체육', '예술', '교양']
sort_order = {'일반': 1, '진로': 2, '융합': 3, '교양': 4}

def get_cat_order(cat):
    if cat in cat_order_list:
        return cat_order_list.index(cat)
    return 99

sem_groups = [g for g, info in groups_info.items() if info["semester"] == current_sem]

for g_name in sem_groups:
    info = groups_info[g_name]
    st.markdown(f"#### {info['title']}")
    st.write(f"최대 **{info['limit']}과목**을 선택해야 합니다. 굵은 글씨의 **(중복)** 과목은 3년 동안 한 번만 수강할 수 있습니다.")
    
    current_count = len(st.session_state[f"selected_{g_name}"])
    if current_count == info['limit']:
        st.success(f"✅ {current_count}/{info['limit']} 선택 완료")
    elif current_count > info['limit']:
        st.error(f"❌ {current_count}/{info['limit']} 초과 선택!")
    else:
        st.info(f"👉 {current_count}/{info['limit']} 선택 중")

    cat_dict = {}
    for subj, tag, cat in subject_list[g_name]:
        if cat not in cat_dict:
            cat_dict[cat] = []
        cat_dict[cat].append((subj, tag))

    sorted_cats = sorted(cat_dict.keys(), key=get_cat_order)

    for cat in sorted_cats:
        items = cat_dict[cat]
        items.sort(key=lambda x: (sort_order.get(x[1], 99), x[0]))
        
        with st.container(border=True):
            st.markdown(f"**🔹 {cat}**")
            cols = st.columns(3) 
            for idx, (subj, tag) in enumerate(items):
                with cols[idx % 3]:
                    display_name = f"**{subj} (중복)**" if subj in overlap_list else subj
                    is_checked = subj in st.session_state[f"selected_{g_name}"]
                    if st.checkbox(f"[{tag}] {display_name}", value=is_checked, key=f"chk_{g_name}_{subj}"):
                        if subj not in st.session_state[f"selected_{g_name}"]:
                            st.session_state[f"selected_{g_name}"].append(subj)
                            st.session_state.is_valid = False
                            st.rerun()
                    else:
                        if subj in st.session_state[f"selected_{g_name}"]:
                            st.session_state[f"selected_{g_name}"].remove(subj)
                            st.session_state.is_valid = False
                            st.rerun()
    st.write("") 

st.markdown("<br>", unsafe_allow_html=True)
col_prev, col_space, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.session_state.current_sem_idx > 0:
        prev_name = semester_tabs[st.session_state.current_sem_idx - 1]
        st.button(f"⬅️ 이전 학기 ({prev_name})", on_click=go_prev, use_container_width=True)

with col_next:
    if st.session_state.current_sem_idx < len(semester_tabs) - 1:
        next_name = semester_tabs[st.session_state.current_sem_idx + 1]
        st.button(f"다음 학기 ({next_name}) ➡️", on_click=go_next, use_container_width=True, type="primary")

st.divider()

# ==========================================
# [본인 선택 과목 확인 및 학점 요약]
# ==========================================
st.subheader("📋 수강 신청 조건 및 선택 과목 확인")
st.write("학교 지정(필수) 과목과 본인이 선택한 과목, 그리고 학점을 최종 확인하세요.")

sum_cols = st.columns(4)
col_idx = 0
for sem in semester_tabs:
    with sum_cols[col_idx]:
        st.markdown(f"**{sem}**")
        sem_subjects = []
        sem_total_credit = 0
        
        if sem in mandatory_subjects:
            for tag, subj, credit in mandatory_subjects[sem]:
                sem_subjects.append({"과목명": f"🔒 {tag} {subj} (지정)", "학점": credit})
                sem_total_credit += credit
                
        for g_name, g_info in groups_info.items():
            if g_info["semester"] == sem:
                group_credit = g_info["credit"]
                for subj in st.session_state[f"selected_{g_name}"]:
                    tag = ""
                    for s, t, c in subject_list[g_name]:
                        if s == subj:
                            tag = t
                            break
                    sem_subjects.append({"과목명": f"✅ [{tag}] {subj}", "학점": group_credit})
                    sem_total_credit += group_credit
        
        if sem_subjects:
            df_display = pd.DataFrame(sem_subjects)
            st.dataframe(df_display, hide_index=True, use_container_width=True)
            st.markdown(f"<div style='text-align: right; color: #004d99; font-weight: bold;'>학기 총합: {sem_total_credit}학점</div>", unsafe_allow_html=True)
        else:
            st.caption("내역 없음")
    col_idx += 1

st.divider()

# ==========================================
# 4. 스마트 사전 진단 로직 및 구글 시트 웹앱 제출
# ==========================================
if st.button("🚀 수강신청 조건 최종 확인하기", use_container_width=True):
    if not st_name.strip():
        st.error("⚠️ 맨 위로 올라가서 성명을 정확히 입력해 주세요.")
    else:
        errors = []
        all_selected = []
        
        for g_name, info in groups_info.items():
            selected = st.session_state[f"selected_{g_name}"]
            all_selected.extend(selected)
            diff = len(selected) - info['limit']
            if diff > 0:
                errors.append(f"🚩 **[{info['semester']} 선택 개수 초과]** \n👉 {info['limit']}과목을 선택해야 하는데 {len(selected)}과목을 선택했습니다. **{diff}과목을 조정**해 주세요.")
            elif diff < 0:
                errors.append(f"🚩 **[{info['semester']} 선택 개수 부족]** \n👉 {info['limit']}과목을 선택해야 하는데 {len(selected)}과목만 선택했습니다. **{-diff}과목을 더 선택**해 주세요.")

        for subj in all_selected:
            if subj in hierarchy_rules:
                pre_subj = hierarchy_rules[subj]
                if pre_subj not in all_selected:
                    errors.append(f"🚩 **[선수 과목 미선택]** \n👉 '{subj}' 수강을 위해 반드시 '{pre_subj}'을(를) 먼저 들어야 합니다. **'{pre_subj}'을(를) 추가**하거나, **'{subj}' 선택을 취소**해 주세요.")
        
        kme_selected = [s for s in all_selected if s in kme_subjects]
        if len(kme_selected) > 8:
            excess = len(kme_selected) - 8
            errors.append(f"🚩 **[국·수·영 이수 한도 초과]** \n👉 다양한 학습을 위해 국·수·영 과목은 최대 8개까지 권장됩니다. 현재 {len(kme_selected)}개 선택되었으니 **{excess}과목을 탐구 등 다른 과목으로 변경**해 보세요.")

        for overlap_subj in overlap_list:
            if all_selected.count(overlap_subj) > 1:
                selected_sems = []
                for g_name, info in groups_info.items():
                    if overlap_subj in st.session_state[f"selected_{g_name}"]:
                        selected_sems.append(info['semester'])
                sem_str = " 및 ".join(selected_sems)
                errors.append(f"🚩 **[중복 선택 확인]** \n👉 '{overlap_subj}' 과목을 **{sem_str}**에 중복으로 선택했습니다. 이 과목은 딱 한 번만 수강 가능하므로 **하나의 학기에서만 선택**해 주세요.")

        tif_selected = [s for s in all_selected if s in tech_info_foreign_subjects]
        if len(tif_selected) < 4:
            shortage = 4 - len(tif_selected)
            errors.append(f"🚩 **[필수 교과 영역 미충족]** \n👉 졸업 요건을 위해 기술·가정/정보/제2외국어/한문 영역에서 최소 4과목 선택이 필요합니다. **해당 영역에서 {shortage}과목을 더 추가**해 주세요.")

        if errors:
            st.session_state.is_valid = False
            show_error_dialog(errors)
        else:
            st.session_state.is_valid = True
            st.rerun()

if st.session_state.is_valid:
    st.success("✅ 축하합니다! 모든 수강신청 조건을 완벽하게 충족했습니다. 아래 버튼을 눌러 데이터를 제출해 주세요.")
    
    if st.button("📥 수강신청 데이터 제출하기", use_container_width=True, type="primary"):
        
        # 📌 선생님의 구글 앱스 스크립트 주소 (완벽 세팅)
        GAS_URL = "https://script.google.com/macros/s/AKfycbz72qQlrmowO96M1CeJZpQhyywFWBS0w1Sq-xud--G42DtYfpg_Ti8p3f-5iQmd2gh4/exec"
        
        def get_sem_str(sem):
            subjs = []
            for g_name, info in groups_info.items():
                if info["semester"] == sem:
                    subjs.extend(st.session_state[f"selected_{g_name}"])
            return ", ".join(subjs)
        
        payload = {
            "class_name": st_class,
            "student_num": st_num,
            "student_name": st_name,
            "sem2_1": get_sem_str("2학년 1학기"),
            "sem2_2": get_sem_str("2학년 2학기"),
            "sem3_1": get_sem_str("3학년 1학기"),
            "sem3_2": get_sem_str("3학년 2학기")
        }
        
        try:
            # 📌 괄호 오류 완벽 해결!
            response = requests.post(GAS_URL, json=payload)
            
            if response.status_code == 200:
                st.balloons()
                st.success(f"🎉 {st_class} {st_num} {st_name} 학생의 수강신청 데이터가 성공적으로 제출되었습니다!")
                st.session_state.is_valid = False 
            else:
                st.error("⚠️ 데이터 제출에 실패했습니다. 선생님께 문의해 주세요.")
        except Exception as e:
            st.error(f"⚠️ 연결 오류가 발생했습니다. (에러: {e})")
