import numpy as np
import pandas as pd
import streamlit as st

def get_statistics():
  # General statistics
  solved = st.session_state.count
  correct = solved - st.session_state.mistakes
  if solved == 0:
    correct_rate = 0
  else:
    correct_rate = correct / solved * 100

  # Top three most mostaken questions
  if len(st.session_state.questions[0]) < 3:
    indices = np.array([0])
    top_3_mistakes = pd.DataFrame(
      np.transpose(np.array(
        [
          st.session_state.questions[0],
          st.session_state.questions[3],
          st.session_state.questions[4],
        ])),
      columns = ["問題", "誤答数", "誤答率"],
    )
  else:
    indices = np.argpartition(st.session_state.questions[4], -3)[-3:]
    top_3_mistakes = pd.DataFrame(
      np.transpose(np.array(
        [
          st.session_state.questions[0][indices],
          st.session_state.questions[3][indices],
          st.session_state.questions[4][indices],
        ])),
      columns = ["問題", "誤答数", "誤答率"],
    )
  return solved, correct, st.session_state.mistakes, correct_rate, top_3_mistakes
