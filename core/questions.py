import numpy as np
import streamlit as st

class List():
  def __init__(self, iterable):
    self._value = list(iterable)
    return

  def __getitem__(self, index):
    return self._value[index]

  def __contains__(self, value):
    return (value in self._value)

  def __repr__(self):
    return repr(self._value)

  def __str__(self):
    return str(self._value)

def check_answer(user_input:str):
  """Checks if the user input matches any registered answer"""
  # Check answer
  correct = st.session_state.questions[1][st.session_state.index]
  result = (user_input.lower() in correct)

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
  """
  Adds new questions and its answers.
  If thre is already the same question, update the answer.
  """
  index = (st.session_state.questions[0] == question.strip().lower())[0]
  if index == -1:
    st.session_state.questions = np.concatenate(
    [
      st.session_state.questions,
      np.array(
        [
          question.strip().lower(),
          [ans.strip().lower() for ans in answers.split(",")],
          0,
          0,
          0,
        ]
      ),
    ],
    1,
  )
  else:
    st.session_state.questions[1, index] = [ans.strip().lower() for ans in answers.split(',')]

  st.success("追加しました")
  return

def delete_question(index:int):
  if len(index) == 0:
    raise ValueError() # To be catched in the main file(streamlit_app.py)
  st.session_state.questions = np.delete(st.session_state.questions, index, 1)
  st.write(st.session_state.questions)
  return
