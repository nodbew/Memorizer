import streamlit as st

# Initialize variables
questions:list[str] = []
answers:list[list[str]] = []

def check_answer(index:int, user_input:str):
  """Checks if the user input matches any registered answer"""
  correct = st.session_state.answers[index]
  return (user_input in correct)

def add_question(question:str, answers:str) -> None:
  """Adds new questions and its answers"""
  st.session_state.questions.append(question)
  st.session_state.answers.append([ans.strip() for ans in answers.split(","))
  return

def delete_question(index:int):
  del st.session_state.questions[index]
  del st.session_state.answers.pop[index]
  return
