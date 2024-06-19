import json
from io import StringIO

import numpy as np
import streamlit as st

@st.cache_data
def to_file():
    return json.dumps(st.session_state.questions.tolist())

def from_file(uploaded:st.UploadedFile):
    uploaded = StringIO(uploaded.getvalue().decode('utf-8')).read()
    try:
        arr = json.loads(uploaded)
        arr = np.array(arr).reshape((5, -1))
        
    except JSONDecodeError:
        st.error('無効なファイル形式です')
        return
        
    except ValueError:
        st.error('無効なファイル形式です')
        return

    st.session_state.questions = np.concatenate([st.session_state.questions, arr], 1)

    # Update counters
    st.session_state.count += np.sum(arr[2:4])
    st.session_state.mistakes += np.sum(arr[3])
    st.rerun()
    return
