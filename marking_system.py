import streamlit as st
import pandas as pd
import os

# फाइल का नाम जहाँ नंबर सेव होंगे
DATA_FILE = "student_marks.csv"

# पेज का टाइटल
st.title("🏫 स्कूल मार्किंग सिस्टम")
st.subheader("शिक्षक द्वारा नंबर एंट्री फॉर्म")

# इनपुट फील्ड्स
with st.form("marks_form"):
    student_name = st.text_input("छात्र का नाम (Student Name)")
    exam_type = st.selectbox("परीक्षा (Exam)", ["Unit Test 1", "Unit Test 2", "Unit Test 3", "Half Yearly"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        hindi = st.number_input("Hindi", min_value=0, max_value=100)
    with col2:
        english = st.number_input("English", min_value=0, max_value=100)
    with col3:
        math = st.number_input("Math", min_value=0, max_value=100)
    
    submitted = st.form_submit_button("नंबर सेव करें")

# डेटा सेव करने का लॉजिक
if submitted:
    new_data = {
        "Name": [student_name],
        "Exam": [exam_type],
        "Hindi": [hindi],
        "English": [english],
        "Math": [math]
    }
    df = pd.DataFrame(new_data)
    
    # अगर फाइल पहले से है तो उसमें जोड़ें, नहीं तो नई बनाएँ
    if not os.path.isfile(DATA_FILE):
        df.to_csv(DATA_FILE, index=False)
    else:
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)
    
    st.success(f"{student_name} के नंबर सफलतापूर्वक सेव हो गए!")

# नीचे सेव किया हुआ डेटा देखें
if os.path.isfile(DATA_FILE):
    st.write("---")
    st.write("### दर्ज किए गए नंबरों की लिस्ट:")
    st.dataframe(pd.read_csv(DATA_FILE))