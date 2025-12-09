import random
import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="たのしい さんすう",
    page_icon="🧮"
)

# --- TITLE ---
st.title("🧮 たのしい さんすう！")
st.write(
    "したの たしざんを といてみよう！  \n"
    "なんもん せいかい できるかな？"
)

# --- INITIALIZE SESSION STATE ---
if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(1, 10)

if "num2" not in st.session_state:
    st.session_state.num2 = random.randint(1, 10)

if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0

if "incorrect_count" not in st.session_state:
    st.session_state.incorrect_count = 0

if "last_message" not in st.session_state:
    st.session_state.last_message = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None  # True / False / None

if "answered" not in st.session_state:
    st.session_state.answered = False


def new_question():
    """あたらしい もんだいを つくる"""
    st.session_state.num1 = random.randint(1, 10)
    st.session_state.num2 = random.randint(1, 10)
    st.session_state.answered = False
    st.session_state.last_result = None
    st.session_state.last_message = ""


# --- SIDEBAR: SCORE ---
with st.sidebar:
    st.header("🎯 スコア")

    st.write(f"✅ せいかい：**{st.session_state.correct_count}**")
    st.write(f"❌ まちがい：**{st.session_state.incorrect_count}**")

    total = st.session_state.correct_count + st.session_state.incorrect_count

    if total > 0:
        accuracy = st.session_state.correct_count / total * 100
        st.write(f"📊 せいかくりつ：**{accuracy:.1f}%**")
    else:
        st.write("📊 せいかくりつ：–")

    if st.button("🔄 スコアと もんだいを リセット"):
        st.session_state.correct_count = 0
        st.session_state.incorrect_count = 0
        new_question()
        st.success("スコアと もんだいを リセットしました！")
        st.rerun()


# --- BUTTONS (HANDLE NEXT FIRST) ---
col1, col2 = st.columns(2)

with col1:
    next_pressed = st.button("➡️ つぎの もんだい")

with col2:
    check_pressed = st.button("✅ こたえを たしかめる")

# If "next problem" was pressed, immediately create new question and rerun
if next_pressed:
    new_question()
    st.rerun()

# --- QUESTION (uses the latest state!) ---
st.subheader("🧠 もんだい")

st.markdown(
    f"**これは いくつかな？**  \n"
    f"`{st.session_state.num1} x {st.session_state.num2} = ?`"
)

# --- ANSWER INPUT ---
answer = st.number_input(
    "こたえを いれてね：",
    min_value=0,
    max_value=100,
    step=1,
)

# --- CHECK ANSWER ---
if check_pressed:
    correct_answer = st.session_state.num1 * st.session_state.num2

    if not st.session_state.answered:
        if answer == correct_answer:
            st.session_state.correct_count += 1
            st.session_state.last_result = True
            st.session_state.last_message = (
                f"🎉 すごい！せいかい！  \n"
                f"{st.session_state.num1} x "
                f"{st.session_state.num2} = {correct_answer} だよ。"
            )
        else:
            st.session_state.incorrect_count += 1
            st.session_state.last_result = False
            st.session_state.last_message = (
                f"😅 おしい！  \n"
                f"{st.session_state.num1} x "
                f"{st.session_state.num2} は "
                f"{correct_answer} だよ。"
            )
        st.session_state.answered = True

# --- FEEDBACK ---
if st.session_state.last_result is True:
    st.success(st.session_state.last_message)
elif st.session_state.last_result is False:
    st.error(st.session_state.last_message)

