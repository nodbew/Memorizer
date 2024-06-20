import json
import numpy as np
from io import StringIO

import numpy as np
import streamlit as st

from . import questions

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super().default(obj)

class CustomListEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, questions.List):
            return obj.getlist()
        else:
            return super().default(obj)

class CustomEncoder(NumpyArrayEncoder, CustomListEncoder):pass

def to_file():
    return json.dumps(st.session_state.questions, cls = CustomEncoder)

def _extend_List_obj(l1:questions.List, l2:questions.List) -> None:
    l1.extend(l2)
    return
_extend_Lists = np.vectorize(_extend_List_obj)

def from_file(uploaded):
    '''
    Takes a st.UploadedFile object, reads it, and adds the data to the questions array.
    '''
    uploaded:str = StringIO(uploaded.getvalue().decode('utf-8')).read()
    try:
        arr:list = json.loads(uploaded)
        arr[1]:list = [questions.List(l) for l in arr[1]]
        arr:np.ndarray = np.array(arr).reshape((5, -1))
        
    except json.JSONDecodeError:
        st.error('無効なファイル形式です')
        return
        
    except ValueError:
        st.error('無効なファイル形式です')
        return

    # Replace overlapping questions' answers with a new concatenated answers list
    questions = np.concatenate([st.session_state.questions, np.array(['\n', [''], 0, 0, 0])], 1) # To absorb all elements that are not overlapping 
    sorter = np.argsort(st.session_state.questions)
    new_arr_indices = sorter[np.searchsorted(st.session_state.questions, arr, sorter = sorter)]
    np.where((new_arr_indices == 0 | new_arr_indices == len(st.session_state.questions), -1, new_arr_indices)) # Replace all indices that are not overlapping with -1

    
    

    st.session_state.questions = np.concatenate([st.session_state.questions, arr], 1)

    # Update counters
    st.session_state.count += np.sum(arr[2:4])
    st.session_state.mistakes += np.sum(arr[3])
    st.rerun()
    return
