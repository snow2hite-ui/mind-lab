
"""Mind Lab: CBT 기반 게임형 감정 탐색 웹앱 (교육용)."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

# ─────────────────────────────
# 1. 앱 기본 설정
# ─────────────────────────────

st.set_page_config(
    page_title="Mind Lab | 마음 연구소",
    page_icon="🪐",
    layout="wide",
)

EMOTIONS = {
    "불안": (
        "😰", "걱정 몬스터",
        "걱정이 떠오를 때는 통제할 수 있는 행동부터 찾아보자.",
    ),
    "슬픔": (
        "🥲", "시무룩 몬스터",
        "지금 느끼는 감정을 억지로 바꿀 필요는 없어.",
    ),
    "분노": (
        "😤", "화산 몬스터",
        "화가 난 이유와 당장 할 행동을 구분해 보자.",
    ),
    "피로": (
        "🫠", "방전 몬스터",
        "조금 쉬는 것도 필요한 선택이야.",
    ),
    "기쁨": (
        "🥳", "반짝 몬스터",
        "좋았던 순간도 기록해 두자.",
    ),
    "평온": (
        "😌", "구름 몬스터",
        "평온한 순간에 도움이 된 것을 살펴보자.",
    ),
}

CONTEXTS = [
    "시험·공부",
    "친구·관계",
    "진로·미래",
    "가족·일상",
    "기타",
]

QUESTS = {
    "불안": "걱정 분류 게임",
    "슬픔": "생각 탐정",
    "분노": "생각 탐정",
    "피로": "1분 회복 퀘스트",
    "기쁨": "나에게 한마디",
    "평온": "나에게 한마디",
}

WORRY_EXAMPLES = {
    "시험·공부": (
        "오늘 공부할 단원 하나 정하기",
        "시험 문제를 정확히 예측하기",
    ),
    "친구·관계": (
        "친구에게 내 마음을 차분히 전하기",
        "친구가 반드시 내 생각에 동의하게 하기",
    ),
    "진로·미래": (
        "궁금한 전공 정보를 찾아보기",
        "미래의 모든 결과를 확실히 알기",
    ),
    "가족·일상": (
        "내가 원하는 것을 구체적으로 말하기",
        "다른 사람의 반응을 완전히 통제하기",
    ),
    "기타": (
        "내가 시도할 수 있는 작은 행동 찾기",
        "다른 사람의 모든 생각을 결정하기",
    ),
}

PAGES = [
    "🏠 홈",
    "💬 감정 체크인",
    "🎮 마음 퀘스트",
    "🕵️ 생각 탐정",
    "📊 마음 리포트",
    "🆘 도움받기",
]

# ─────────────────────────────
# 2. 화면 디자인
# ─────────────────────────────

st.markdown("""
<style>
.block-container {
    max-width: 1000px;
    padding-top: 1.7rem;
}
.hero {
    background: linear-gradient(120deg, #eee4fc, #e0f5ef);
    padding: 27px;
    border-radius: 22px;
}
.hero h1 {
    color: #43375d;
    margin: 0 0 8px 0;
}
.hero p {
    color: #5b5670;
    margin: 0;
}
.monster {
    text-align: center;
    background: #f5f0ff;
    border-radius: 20px;
    padding: 25px;
}
.monster .face {
    font-size: 75px;
}
.monster h3 {
    color: #554773;
}
[data-testid="stSidebar"] {
    background: #f7f4fc;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# 3. 세션 데이터 초기화
# ─────────────────────────────

if "records" not in st.session_state:
    st.session_state.records = []

if "pending" not in st.session_state:
    st.session_state.pending = None

if "page" not in st.session_state:
    st.session_state.page = PAGES[0]


def navigate(destination):
    st.session_state.page = destination


def support_info():
    st.error(
        "지금 즉각적인 위험이 있거나 스스로를 해칠 가능성이 "
        "있다면 앱 대신 주변 사람과 전문기관의 도움을 요청하세요."
    )

    a, b, c = st.columns(3)
    a.metric("긴급 구조", "119")
    b.metric("경찰 신고", "112")
    c.metric("자살예방상담", "109")

    st.info(
        "청소년상담: 1388 (전화·온라인 상담). "
        "위험하지 않더라도 도움을 요청할 수 있습니다."
    )

    st.markdown(
        "[청소년1388 상담 안내](https://www.1388.go.kr/)"
    )
    st.caption(
        "이 앱은 위기를 감지하거나 판별하지 못합니다. "
        "위 연락처는 도움이 필요할 때 직접 이용할 수 있도록 "
        "제공하는 정보입니다."
    )


def save_activity(quest, after):
    pending = st.session_state.pending

    if pending is None:
        st.warning(
            "리포트에 남기려면 먼저 감정 체크인을 해 주세요."
        )
        return

    record = {
        "일시": datetime.now(
            ZoneInfo("Asia/Seoul")
        ).strftime("%Y-%m-%d %H:%M"),
        "감정": pending["emotion"],
        "상황": pending["context"],
        "활동": quest,
        "활동 전 강도": pending["before"],
        "활동 후 강도": after,
    }

    st.session_state.records.append(record)
    st.session_state.pending = None

    st.success(
        "활동 기록 완료! 🌟 참여 스티커 1개를 획득했어요."
    )
    st.caption(
        "강도 변화는 자기보고 결과이며, 치료 효과를 뜻하지 않습니다."
    )


def finish_control(quest):
    st.divider()

    if st.session_state.pending:
        before = st.session_state.pending["before"]
    else:
        before = 5

    after = st.slider(
        "활동 후 같은 감정의 강도 (0~10)",
        0, 10, before,
        key=f"after_{quest}",
    )

    if st.button(
        "활동 완료하고 기록하기 🌟",
        type="primary",
        key=f"finish_{quest}",
    ):
        save_activity(quest, after)


# ─────────────────────────────
# 4. 사이드바 메뉴
# ─────────────────────────────

with st.sidebar:
    st.title("🪐 Mind Lab")
    st.caption("마음을 탐색하는 작은 연구소")

    st.radio("메뉴", PAGES, key="page")

    st.divider()

    st.caption(
        "교육용 자기관리 프로그램 · 심리치료/진단 아님"
    )

    if st.button(
        "🗑️ 이번 접속 기록 모두 삭제",
        use_container_width=True,
    ):
        st.session_state.records = []
        st.session_state.pending = None
        st.success("이번 접속의 활동 기록을 삭제했어요.")

    st.caption(
        "입력 데이터는 서버 세션 메모리에서 처리됩니다. "
        "별도 DB나 외부 AI API에 저장하지 않습니다. "
        "공개 배포 시 호스팅 환경의 개인정보 정책을 확인하세요."
    )

page = st.session_state.page

# ─────────────────────────────
# 5. 홈 화면
# ─────────────────────────────

if page == PAGES[0]:

    st.markdown(
        """
        <div class="hero">
          <h1>내 마음을 탐험하는 연구소 🪐</h1>
          <p>
            감정을 관찰하고, 생각을 탐정처럼 살펴보고,
            짧은 퀘스트를 해 보세요.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    a, b, c = st.columns(3)

    a.metric(
        "기록한 감정",
        f"{len(st.session_state.records)}회",
    )

    b.metric(
        "참여 스티커",
        f"{len(st.session_state.records)}개",
    )

    unique_quests = {
        r["활동"] for r in st.session_state.records
    }

    c.metric(
        "체험 활동 종류",
        f"{len(unique_quests)}개",
    )

    st.subheader("오늘의 마음 탐험")

    st.write(
        "**① 감정 체크인** → **② 맞춤형 퀘스트** "
        "→ **③ 생각 탐정** → **④ 마음 리포트**"
    )

    st.button(
        "감정 체크인 시작",
        type="primary",
        on_click=navigate,
        args=(PAGES[1],),
    )

    st.info(
        "이 앱은 심리학의 생각 기록 구조를 활용한 "
        "학습용 자기성찰 도구입니다. "
        "실제 상담사나 의료 전문가를 대신하지 않습니다."
    )

# ─────────────────────────────
# 6. 감정 체크인
# ─────────────────────────────

elif page == PAGES[1]:

    st.title("💬 감정 체크인")
    st.write(
        "오늘의 기분과 그 배경을 직접 선택해 주세요. "
        "AI가 마음을 진단하지 않습니다."
    )

    with st.form("checkin_form"):

        emotion = st.selectbox(
            "지금 가장 가까운 감정",
            list(EMOTIONS),
        )

        context = st.selectbox(
            "감정이 생긴 상황",
            CONTEXTS,
        )

        strength = st.slider(
            "지금 느끼는 감정의 강도",
            0, 10, 5,
        )

        need_help = st.checkbox(
            "지금 안전하지 않거나 "
            "즉시 누군가의 도움이 필요해요"
        )

        submitted = st.form_submit_button(
            "내 감정 몬스터 만나기 👾",
            type="primary",
        )

    if submitted:

        if need_help:
            st.session_state.pending = None
            navigate(PAGES[5])
            st.rerun()

        st.session_state.pending = {
            "emotion": emotion,
            "context": context,
            "before": strength,
        }

    pending = st.session_state.pending

    if pending:

        emoji, title, message = EMOTIONS[
            pending["emotion"]
        ]

        left, right = st.columns([1, 1.5])

        with left:
            st.markdown(
                f"""
                <div class="monster">
                  <div class="face">{emoji}</div>
                  <h3>{title}</h3>
                  <p>{message}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:

            recommended = QUESTS[
                pending["emotion"]
            ]

            st.subheader(
                f"추천 퀘스트: {recommended}"
            )

            st.write(
                f"선택한 상황: **{pending['context']}**"
            )

            st.write(
                f"활동 전 감정 강도: "
                f"**{pending['before']}/10**"
            )

            st.caption(
                "추천은 감정별 고정 규칙을 이용합니다. "
                "사용자가 다른 활동을 골라도 됩니다."
            )

            st.button(
                "퀘스트 시작 →",
                type="primary",
                on_click=navigate,
                args=(PAGES[2],),
            )

# ─────────────────────────────
# 7. 마음 퀘스트
# ─────────────────────────────

elif page == PAGES[2]:

    st.title("🎮 마음 퀘스트")

    pending = st.session_state.pending

    if not pending:
        st.warning(
            "감정 체크인 없이 활동을 체험할 수 있지만 "
            "결과는 리포트에 기록되지 않습니다."
        )

    if pending:
        default = QUESTS[pending["emotion"]]
    else:
        default = "걱정 분류 게임"

    choices = [
        "걱정 분류 게임",
        "생각 탐정",
        "1분 회복 퀘스트",
        "나에게 한마디",
    ]

    quest = st.selectbox(
        "활동을 선택하세요",
        choices,
        index=choices.index(default),
    )

    # 생각 탐정으로 이동
    if quest == "생각 탐정":

        st.write(
            "사실과 생각을 구분하는 CBT 기반 "
            "생각 기록을 작성해 봅시다."
        )

        st.button(
            "생각 탐정으로 이동 🕵️",
            on_click=navigate,
            args=(PAGES[3],),
            type="primary",
        )

    # 걱정 분류 게임
    elif quest == "걱정 분류 게임":

        st.subheader(
            "🗂️ 바꿀 수 있는 것과 없는 것"
        )

        context = (
            pending["context"]
            if pending else "기타"
        )

        controllable, uncontrollable = (
            WORRY_EXAMPLES[context]
        )

        st.write(
            "**카드 A:**",
            controllable,
        )

        answer1 = st.radio(
            "카드 A는?",
            [
                "내가 시도할 수 있는 행동",
                "내가 확정할 수 없는 결과",
            ],
            key="q1",
        )

        st.write(
            "**카드 B:**",
            uncontrollable,
        )

        answer2 = st.radio(
            "카드 B는?",
            [
                "내가 시도할 수 있는 행동",
                "내가 확정할 수 없는 결과",
            ],
            key="q2",
        )

        if st.button("분류 결과 확인"):

            if (
                answer1 == "내가 시도할 수 있는 행동"
                and answer2 == "내가 확정할 수 없는 결과"
            ):
                st.success(
                    "두 카드를 잘 구분했어요! 🏅"
                )
            else:
                st.info(
                    "A는 시도 가능한 행동, "
                    "B는 결과를 확정할 수 없는 "
                    "상황에 가까워요."
                )

        finish_control(quest)

    # 휴식 퀘스트
    elif quest == "1분 회복 퀘스트":

        st.subheader(
            "🌿 짧은 회복 미션"
        )

        st.radio(
            "지금 선택할 수 있는 행동",
            [
                "물 한 잔 마시기",
                "가볍게 스트레칭하기",
                "주변의 사물 다섯 가지 관찰하기",
                "잠깐 화면에서 눈 떼기",
            ],
        )

        done = st.checkbox(
            "활동을 시도했거나, "
            "시도할 행동을 정했어요"
        )

        if done:
            finish_control(quest)

    # 자기친절 퀘스트
    elif quest == "나에게 한마디":

        st.subheader(
            "💌 자기친절 카드"
        )

        st.radio(
            "오늘 나에게 건네고 싶은 말",
            [
                "오늘 모든 것을 해결할 필요는 없어.",
                "실수해도 다시 시도할 수 있어.",
                "쉬는 시간도 중요해.",
                "내가 느끼는 감정을 존중해 보자.",
            ],
        )

        if st.checkbox(
            "선택한 문장을 천천히 읽어 봤어요"
        ):
            finish_control(quest)

# ─────────────────────────────
# 8. 생각 탐정: CBT 기반 7단계
# ─────────────────────────────

elif page == PAGES[3]:

    st.title(
        "🕵️ 생각 탐정 — CBT 생각 기록"
    )

    st.write(
        "상황과 그에 대한 해석을 분리하고, "
        "다양한 가능성을 살펴보는 7단계 연습입니다."
    )

    st.caption(
        "영국 NHS의 Thought Record 구조를 참고한 "
        "교육용 활동입니다. "
        "가상의 상황으로 연습해도 됩니다."
    )

    with st.expander("✍️ 작성 예시"):

        st.write(
            "사실: 친구가 내 메시지를 읽었지만 "
            "답하지 않았다."
        )
        st.write(
            "떠오른 생각: 나를 싫어하나?"
        )
        st.write(
            "다른 가능성: 바빠서 나중에 "
            "답하려는 걸 수도 있다."
        )

    with st.form(
        "thought_form",
        clear_on_submit=True,
    ):

        situation = st.text_area(
            "① 실제로 무슨 일이 있었나요? "
            "(상황·사실)",
            max_chars=400,
        )

        feeling = st.text_input(
            "② 그때 느낀 감정은 무엇인가요?",
            max_chars=100,
        )

        thought = st.text_area(
            "③ 순간적으로 어떤 생각이 떠올랐나요?",
            max_chars=400,
        )

        support = st.text_area(
            "④ 그 생각을 뒷받침하는 사실이 있나요?",
            max_chars=400,
        )

        against = st.text_area(
            "⑤ 다른 해석이 가능하다는 근거는 없나요?",
            max_chars=400,
        )

        balance = st.text_area(
            "⑥ 지금 떠올릴 수 있는 "
            "보다 균형 잡힌 해석은?",
            max_chars=400,
        )

        st.caption(
            "정답이 있는 활동이 아닙니다. "
            "모든 고민을 긍정적으로 "
            "해석할 필요는 없습니다."
        )

        before = (
            st.session_state.pending["before"]
            if st.session_state.pending else 5
        )

        after = st.slider(
            "⑦ 지금 같은 감정의 강도 (0~10)",
            0, 10, before,
        )

        submitted = st.form_submit_button(
            "생각 탐정 활동 완료 🏅",
            type="primary",
        )

    if submitted:

        if not (
            situation.strip()
            and thought.strip()
            and balance.strip()
        ):
            st.warning(
                "상황(①), 떠오른 생각(③), "
                "다시 살펴본 생각(⑥)을 "
                "입력해 주세요."
            )

        else:

            st.success(
                "7단계 활동을 마쳤어요. "
                "감정 강도가 그대로여도 괜찮아요."
            )

            st.caption(
                "작성한 글은 데이터베이스나 "
                "리포트에 저장하지 않습니다. "
                "서버의 입력 위젯에서 "
                "일시적으로 처리됩니다."
            )

            save_activity(
                "생각 탐정",
                after,
            )

# ─────────────────────────────
# 9. 마음 데이터 리포트
# ─────────────────────────────

elif page == PAGES[4]:

    st.title("📊 마음 리포트")

    st.caption(
        "지금 접속 세션에서 사용자가 "
        "선택한 감정을 집계합니다. "
        "임상 검사나 진단 결과가 아닙니다."
    )

    if not st.session_state.records:

        st.info(
            "아직 완료한 활동이 없습니다. "
            "체크인과 퀘스트를 진행해 보세요."
        )

    else:

        df = pd.DataFrame(
            st.session_state.records
        )

        a, b = st.columns(2)

        a.metric(
            "기록한 활동",
            f"{len(df)}회",
        )

        b.metric(
            "탐색한 감정 종류",
            f"{df['감정'].nunique()}개",
        )

        st.subheader(
            "감정별 기록 횟수"
        )

        st.bar_chart(
            df["감정"].value_counts()
        )

        st.subheader(
            "활동 전후 자기보고 강도"
        )

        st.line_chart(
            df[
                [
                    "활동 전 강도",
                    "활동 후 강도",
                ]
            ].reset_index(drop=True)
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "내 기록 CSV 저장",
            data=df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="mindlab_records.csv",
            mime="text/csv",
        )

        st.caption(
            "강도의 증가·감소만으로 활동 효과를 "
            "판단할 수 없습니다. 서로 다른 감정의 "
            "강도를 건강 점수처럼 합산하지 않습니다."
        )

# ─────────────────────────────
# 10. 전문 상담 안내
# ─────────────────────────────

elif page == PAGES[5]:

    st.title("🆘 도움이 필요할 때")

    st.write(
        "고민을 혼자 해결하기 어렵다면 "
        "신뢰할 수 있는 어른, 학교 상담실 "
        "또는 전문 상담기관에 "
        "도움을 요청할 수 있어요."
    )

    support_info()

    st.subheader(
        "이 앱이 할 수 없는 일"
    )

    st.write(
        "- 정신질환 진단 및 치료\n"
        "- 자해·자살 위험도의 정확한 평가\n"
        "- 전문 상담사의 역할 대체\n"
        "- 상담 내용에 대한 비밀 보장 수준의 "
        "전문 서비스"
    )

# ─────────────────────────────
# 11. 하단 안내
# ─────────────────────────────

st.divider()

st.caption(
    "Mind Lab · 고등학교 바이브코딩 프로젝트 | "
    "사용자에게 감정 선택권을 제공하는 "
    "비임상 학습용 웹앱"
)
