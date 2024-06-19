import numpy as np
import streamlit as st

class List(list):
  def __init__(self, iterable):
    super().__init__(iterable)
    return

def check_answer(user_input:str):
  """Checks if the user input matches any registered answer"""
  # Check answer
  correct = st.session_state.questions[1][st.session_state.index]
  result = (user_input in correct)

  # Update counts
  questions = st.session_state.questions
  index = st.session_state.index
  if correct:
    questions[2][index] += 1
  else:
    questions[3][index] += 1
    
  questions[4][index] = int(questions[3][index] / (questions[2][index] + questions[3][index]))

  return result

def add_question(question:str, answers:str) -> None:
  """Adds new questions and its answers"""
  st.session_state.questions = np.concatenate(
    [
      st.session_state.questions,
      np.array(
        [
          question,
          [ans.strip() for ans in answers.split(",")],
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
  del st.session_state.questions[:, index]
  return
