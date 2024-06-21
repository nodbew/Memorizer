import json
import numpy as np
from io import StringIO

import numpy as np
import streamlit as st

from .questions import List

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super().default(obj)

class CustomListEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, List):
            return obj.getlist()
        else:
            return super().default(obj)

class CustomEncoder(NumpyArrayEncoder, CustomListEncoder):pass

def to_file():
    return json.dumps(st.session_state.questions, cls = CustomEncoder)

def _extend_List_obj(l1:List, l2:List) -> None:
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
        arr[1]:list = [List(l) for l in arr[1]]
        arr:np.ndarray = np.array(arr).reshape((5, -1))
        
    except json.JSONDecodeError:
        st.error('無効なファイル形式です')
        return
        
    except ValueError:
        st.error('無効なファイル形式です')
        return

    # Replace overlapping questions' answers with a new concatenated answers list
    overlapping_old_arr_indices = np.isin(st.session_state.questions, arr, assume_unique = True)
    overlapping_new_arr_indices = np.isin(arr, st.session_state.questions, assume_unique = True)
    # The arrays should be sorted
    _extend_Lists(st.session_state.questions[overlapping_old_arr_indices], arr[overlapping_new_arr_indices])
    del arr[overlapping_new_arr_indices] # Delete unneeded columnd

    # Concatenate arrays
    questions = np.concatenate(st.session_state.questions, arr)
    st.session_state.questions = questions[np.argsort(questions[0])]

    # Update counts
    st.session_state.count += np.sum(arr[2:4])
    st.session_state.mistakes += np.sum(arr[4])

    # Delete old datas
    if -1 not in old_arr_indices:
        del st.session_state.qestions[-1]
    del st.session_state.questions[old_arr_indices]

    st.session_state.questions = np.concatenate([st.session_state.questions, arr], 1)

    # Update counters
    st.session_state.count += np.sum(arr[2:4])
    st.session_state.mistakes += np.sum(arr[3])
    st.rerun()
    return
