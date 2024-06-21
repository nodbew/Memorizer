import random

import numpy as np
import pandas as pd
import streamlit as st

import core.questions as questions
import core.statistics as stats
import core.datas as datas

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
    ,dtype = 'object')
if "count" not in st.session_state:
    st.session_state.count = 0
if "mistakes" not in st.session_state:
    st.session_state.mistakes = 0
if "index" not in st.session_state:
    st.session_state.index = 0
if "input" not in st.session_state:
    st.session_state.input = ""
if 'last_uploaded_file_name' not in st.session_state:
    st.session_state.last_uploaded_file_name = ''

main, add, statistics, files = st.tabs(["出題", "問題集", "成績", '保存'])

with main:
    if len(st.session_state.questions[0]) == 0:
        st.error('問題がありません  \n問題を追加してください')
    else:
        st.write(st.session_state.questions[0][st.session_state.index])   
        st.session_state.input = st.text_input(label = "答え")


        if st.button("答える"):
            result = questions.check_answer(st.session_state.input)
            
            if result:
                st.success("正解！")
                st.session_state.questions[2][st.session_state.index] += 1
            else:
                st.session_state.mistakes += 1
                st.session_state.questions[3][st.session_state.index] += 1
                st.error(f"不正解...正解は{st.session_state.questions[1][st.session_state.index]}")

            st.session_state.count += 1
            st.session_state.questions[4][st.session_state.index] = round(
                st.session_state.questions[3][st.session_state.index] / (
                    st.session_state.questions[2][st.session_state.index] + st.session_state.questions[3][st.session_state.index]
                ) * 100
            )
                
        if st.button('次へ'):
            st.session_state.index = random.randrange(0, len(st.session_state.questions[0]))
            st.rerun()

with add:
    st.header("問題追加")
    question = st.text_input(label = "問題", value = "Hello")
    st.info("答えは、で区切って入れてください")
    answers = st.text_input(label = "答え", value = "こんにちは、こんばんは")
    if st.button("追加"):
        questions.add_question(question, answers)

    st.header("問題の削除")
    target = st.text_input(label = "問題文", value = "削除したい問題を入力...")
    if st.button("削除"):
        try:
            questions.delete_question(np.where(st.session_state.questions[0] == target.strip().lower())[0])
            st.success('削除しました')
            st.session_state.index = random.randrange(0, len(st.session_state.questions[0]))
            st.rerun()
        except ValueError:
            st.error("その問題はありません")

    if len(st.session_state.questions[0]) > 0:
        st.header('問題一覧')
        st.dataframe(pd.DataFrame(
            st.session_state.questions.T,
            columns = ['問題', '解答', '正答数', '誤答数', '誤答率'],
        ))

with statistics:
    solved, correct, mistakes, correct_rate, top3 = stats.get_statistics()
    st.write(f"累計回答数:{solved}問")
    st.write(f"累計正解数:{correct}問")
    st.write(f"累計誤答数:{mistakes}問")
    st.write(f"正答率:{correct_rate}％")
    st.dataframe(top3)
    if st.button("更新"):pass # For refreshing

with files:
    st.info('問題データや成績などが保存されます')
    if len(st.session_state.questions[0]) > 0:
        name = f'Memorizer-Data-{st.session_state.questions[0][st.session_state.index]}.json'
    else:
        name = 'Memorizer-Data.json'
    st.download_button(
        label = 'ダウンロード', 
        data = datas.to_file(), 
        file_name = name,
    )
    uploaded = st.file_uploader(label = 'アップロード')
    if uploaded is not None and uploaded.name != st.session_state.last_uploaded_file_name:
        st.session_state.last_uploaded_file_name = uploaded.name
        datas.from_file(uploaded)
