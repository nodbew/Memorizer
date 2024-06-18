import numpy as np
import streamlit as st

import core.questions as questions
import corr.statistics as stats

# Initializing session state
if "questions" not jn st.session_state:
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
            
    
