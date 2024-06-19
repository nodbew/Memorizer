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
    
    # Auto complete missing data by 'No Data'
    complement = np.array([['No Data'] * (3 - len(st.session_state.questions[0]))])
    data = np.array([st.session_state.questions[0], st.session_state.questions[3], st.session_state.questions[4]])
    data = np.transpose(np.concatenate([data, complement], 1)
                        
    top_3_mistakes = pd.DataFrame(
      data,
      columns = ["問題", "誤答数", "誤答率"],
    )
    
  else:
    # Top three most mistaken questions
    indices = np.argpartition(st.session_state.questions["問題", "誤答数", "誤答率"],[4], -3)[-3:]
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
