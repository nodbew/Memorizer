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
    questions = np.concatenate([st.session_state.questions, np.array([['\n'], [List([])], [0], [0], [0]])], 1) # To absorb all elements that are not overlapping 
    sorter = np.argsort(st.session_state.questions)
    old_arr_indices = sorter[np.searchsorted(st.session_state.questions, arr, sorter = sorter)]
    old_arr_indices = np.where((old_arr_indices == 0 | old_arr_indices == len(st.session_state.questions), -1, old_arr_indices)) # Replace all indices that are not overlapping with -1

    # Replace answers
    old_overlapping_array = st.session_state.questions[:, old_arr_indices]
    _extend_Lists(arr[1], old_overlapping_array[1])

    # Update counts
    arr[2:4] += old_overlapping_array[2:4]
    arr[4] = np.round(arr[3] / (arr[2] + arr[3]))

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
