import numpy as np
import streamlit as st

def check_answer(user_input:str):
  """Checks if the user input matches any registered answer"""
  correct = st.session_state.questions[1][st.session_state.index]
  return (user_input in correct)

def add_question(question:str, answers:str) -> None:
  """Adds new questions and its answers"""
  st.session_state.questions = np.concatenate(
    [
      st.session_state.questions,
      np.array(
        [
          question,
          [ans.strip() for ans in answers.split(","),
          0,
          0,
          0,
        ]
      ),
    ],
    1,
  )
      
  return

def delete_question(index:int):
  del st.session_state.questions[index]
  del st.session_state.answers.pop[index]
  return
