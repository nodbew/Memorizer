import numpy as np
import streamlit as st

import core.questions as questions
import core.statistics as stats

# Initializing session state
if "questions" not in st.session_state:
    st.session_state.questions = np.array(
        [
    [], # Questions:list[str]
    [], # Answers:list[list[str]]
    [], # Count of correct answerinngs:[list[int]]
    [], # Count of mistakes:list[int]
    [], # Mistake rate:int
        ]
    )
if "count" not in st.session_state:
    st.session_state.count = 0
if "mistakes" not in st.session_state:
    st.session_state.mistakes = 0
if "index" not in st.session_state:
    st.session_state.index = 0
if "input" not in st.session_state:
    st.session_state.input = ""
if "wait" not in st.session_state:
    st.session_state.wait = False

main, add, statistics = st.tabs(["出題", "問題集", "成績"])
with main:
    if st.session_state.wait:
        st.write(st.session_state.questions[0][st.session_state.index])
        st.write(st.session_state.input)
        if st.button("次へ"):
            st.session_state.wait = False
            st.rerun()
    else:
        st.session_state.index = random.randint(0, len(st.session_state.questions[0]))
        st.write(st.session_state.questions[0][st.session_state.index])
        st.session_state.input = st.text_input(label = "答え")
        if st.button("答える"):
            result = questions.check_answer(st.session_state.input)
            if result:
                st.success("正解！")
            else:
                st.error(f"不正解...正解は{st.session_state.questions[1][st.session_state.index]}")
            st.session_state.wait = True

with add:
    st.header("問題追加")
    question = st.text_input(label = "問題", value = "Hello")
    st.info("答えは、で区切って入れてください")
    answers = st.text_input(label = "答え", value = "こんにちは、こんばんは")
    if st.button("追加"):
        question.add_auestion(question, answers)

    st.header("問題の削除")
    target = st.text_input(label = "問題文", value = "削除したい問題を入力...")
    if st.button("削除"):
        try:
            questions.delete_question(st.session_state.questions[0].index(target))
            st.success("削除しました")
        except ValueError:
            st.error("その問題はありません")

with statistics:
    solved, correct, mistakes, correct_rate, top3 = stats.get_statistics()
    st.write(f"累計回答数:{solved}")
    st.write(f"累計正解数:{correct}")
    st.write(f"累計誤答数:{mistakes}")
    st.write(f"正答率:{correct_rate}")
    st.dataframe(top3)
    if st.button("更新"):pass # For refreshing
