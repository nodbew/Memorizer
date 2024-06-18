import streamlit as st

# Initialize variables
questions:list[str] = []
answers:list[list[str]] = []

def check_answer(index:int, user_input:str):
  """Checks if the user input matches any registered answer"""
  correct = st.session_state.answers[index]
  return user_input in correct
  return False

def update_data(question:str, answers:str) -> None:
  """Updates the questions and answers lists"""
  questions.append(question)
  answers.append([ans.strip() for ans in answers.split(","))
  return
