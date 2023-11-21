import streamlit as st
import selectionLists as sl

st.title('Frequency Selectbox Test')

if 'frequencyDict' not in st.session_state:
    st.session_state['frequencyDict'] = sl.frequency_dict

# Test selectbox at the start
test_freq = st.selectbox('Test Frequency', list(st.session_state['frequencyDict'].keys()))
st.write("Selected frequency:", test_freq)
