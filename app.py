import streamlit as st
import pandas as pd
import io

# --- 1. CONFIG & STYLING (Premium Look) ---
st.set_page_config(page_title="School Marking System Pro", layout="wide")
st.markdown("""
    <style>
    .marksheet-box { border: 8px double #1a5f7a; padding: 25px; background-color: #fff; width: 850px; margin: auto; box-shadow: 0 0 20px rgba(0,0,0,0.2); font-family: Arial; }
    .school-header { background-color: yellow; padding: 10px; border-radius: 10px; border: 2px solid #000; margin-bottom: 5px; }
    .school-name { font-size: 32px; font-weight: bold; text-align: center; text-transform: uppercase; color: #d32f2f; margin:0; }
    .address { text-align: center; font-size: 15px; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; font-weight: bold; }
    .info-container { display: flex; justify-content: space-between; margin-bottom: 20px; font-size: 14px; line-height: 1.8; }
    .info-left { width: 55%; }
    .info-right { width: 40%; text-align: left; padding-left: 20px; border-left: 1px dashed #ccc; }
    .marks-table { width: 100%; border-collapse: collapse; margin-bottom: 5px; }
    .marks-table th { background-color: #1a5f7a; color: white; border: 1px solid #000; padding: 6px; text-align: center; }
    .marks-table td { border: 1px solid #000; padding: 6px; text-align: center; font-size: 12px; font-weight: bold; }
    .max-val { color: #d32f2f; } .obt-val { color: #2e7d32; } .gt-val { color: #d32f2f; font-weight: bold; }
    .total-row { background-color: #eee; font-weight: bold; }
    .result-section { border: 2px solid #000; padding: 10px; margin-top: 15px; display: flex; justify-content: space-around; font-weight: bold; font-size: 15px; background: #e3f2fd; }
    .footer-sig { display: flex; justify-content: space-between; margin-top: 60px; font-weight: bold; text-align: center; } .sig-box { width: 200px; } .sig-font { font-family: 'Lucida Handwriting', 'Brush Script MT', cursive; font-size: 30px; font-weight: normal; margin-bottom: -5px; }
    .fail-text { color: red; font-weight: bold; }
   @media print {
    /* 1. प्रिंट में बटन, साइडबार और हेडर को गायब करने के लिए */
    header, [data-testid="stSidebar"], .stButton, button, .stInfo, .stSuccess { 
        display: none !important; 
    }
    
    /* 2. पेज को Landscape (आड़ा) और A4 साइज में सेट करने के लिए */
    @page { size: A4 landscape; margin: 10mm; }

    /* 3. मार्कशीट बॉक्स को पूरे पेज पर फिट करने के लिए */
    .marksheet-box { 
        width: 100% !important; 
        border: 4px double #000 !important; 
        box-shadow: none !important;
        page-break-inside: avoid;
    }
}
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGIC FUNCTIONS ---
def get_division(per):
    if per >= 60: return "FIRST DIV."
    elif per >= 48: return "SECOND DIV."
    elif per >= 36: return "THIRD DIV."
    else: return "FAIL"

def calculate_grade(marks_per):
    if marks_per >= 91: return "A+"
    elif marks_per >= 75: return "A"
    elif marks_per >= 60: return "B"
    elif marks_per >= 45: return "C"
    elif marks_per >= 33: return "D"
    else: return "E"

# --- 3. SIDEBAR & CLASS ---
school = st.sidebar.text_input("School Name", "ABC SCHOOL, PAOTA")
addr = st.sidebar.text_input("Address", "Main Road, Paota, Jaipur")
phone = st.sidebar.text_input("Contact", "9999999999")

selected_class = st.selectbox("क्लास चुनें:", ["Nursery", "LKG", "UKG", "1", "2", "3", "4", "6", "7", "9", "11"])
key_class = selected_class
if selected_class == "11":
    stream = st.radio("संकाय (Stream):", ["Science", "Commerce", "Arts", "Agri"], horizontal=True)
    key_class = f"11_{stream}"

# --- 4. SUBJECT SETUP ---
st.header("1. Setup Subjects")
c1, c2 = st.columns(2)
m_count = c1.number_input("Main Subjects (Max 6)", 1, 6, 6)
o_count = c2.number_input("Other Subjects (Max 4)", 0, 4, 2)

m_col, o_col = st.columns(2)
with m_col:
    main_df = st.data_editor(pd.DataFrame({"Subject": [""] * m_count, "T1_M": 10, "T2_M": 10, "T3_M": 10, "HY_M": 70, "YR_M": 100}), key=f"ms_{key_class}")
with o_col:
    other_df = st.data_editor(pd.DataFrame({"Other Subject": [""] * o_count}), key=f"os_{key_class}")

# --- 5. STUDENT DETAILS (Excel Upload/Manual) ---
st.header("2. Student Details")
cols = ["S.R. No", "Exam R.N.", "Student Name", "Father's Name", "Mother's Name", "Date of Birth", "Section", "Gender", "Caste"]
uploaded_file = st.file_uploader("Upload Student Excel", type=["xlsx"])

if uploaded_file:
    profile_df = pd.read_excel(uploaded_file)
    profile_df.columns = [c.strip() for c in profile_df.columns]
    profile_df = st.data_editor(profile_df, num_rows="dynamic", key=f"pe_{key_class}")
    profile_df["Date of Birth"] = pd.to_datetime(profile_df["Date of Birth"], dayfirst=True, errors='coerce').dt.strftime('%d-%m-%Y')
else:
    profile_df = st.data_editor(pd.DataFrame("", index=range(5), columns=cols), num_rows="dynamic", key=f"pe_manual_{key_class}")

# --- 6. MARKS ENTRY & MARKSHEET ---
active_indices = profile_df[profile_df["Student Name"].astype(str).str.strip() != ""].index.tolist()

if active_indices and any(main_df["Subject"] != ""):
    st.header("3. Enter Marks & Preview")
    sel_idx = st.selectbox("बच्चा चुनें:", active_indices, format_func=lambda x: profile_df.at[x, "Student Name"])
    s_data = profile_df.loc[sel_idx]
    
    m_list = main_df[main_df["Subject"] != ""].to_dict('records')
    m_entry = st.data_editor(pd.DataFrame({"Subject": [x['Subject'] for x in m_list], "T1":0, "T2":0, "T3":0, "HY":0, "YR":0}), key=f"marks_{sel_idx}")

    # Strict Validation
    for i, row in m_entry.iterrows():
        limits = m_list[i]
        for ex in ["T1", "T2", "T3", "HY", "YR"]:
            if float(row[ex]) > float(limits[f"{ex}_M"]):
                st.error(f"❌ {row['Subject']} limit is {limits[f'{ex}_M']}!")
                m_entry.at[i, ex] = 0

    if st.button(f"👁️ Preview Marksheet"):
        g_tot, m_tot, min_tot = 0, 0, 0
        t1, t2, t3, hy, yr = 0, 0, 0, 0, 0
        m_html = ""
        is_failed = False
        
        for i, r in m_entry.iterrows():
            stot = sum([r['T1'], r['T2'], r['T3'], r['HY'], r['YR']])
            smax = sum([m_list[i]['T1_M'], m_list[i]['T2_M'], m_list[i]['T3_M'], m_list[i]['HY_M'], m_list[i]['YR_M']])
            pass_m = round(smax * 0.36)
            g_tot += stot; m_tot += smax; min_tot += pass_m
            t1+=r['T1']; t2+=r['T2']; t3+=r['T3']; hy+=r['HY']; yr+=r['YR']
            
            f_tag = " <span class='fail-text'>(F)</span>" if stot < pass_m else ""
            if stot < pass_m: is_failed = True
            m_html += f"<tr><td>{r['Subject']}</td><td class='max-val'>{smax}</td><td>{pass_m}</td><td>{r['T1']}</td><td>{r['T2']}</td><td>{r['T3']}</td><td>{r['HY']}</td><td>{r['YR']}</td><td class='obt-val'>{stot}{f_tag}</td></tr>"

        m_html += f"<tr class='total-row'><td>GRAND TOTAL</td><td class='gt-val'>{m_tot}</td><td>{min_tot}</td><td>{t1}</td><td>{t2}</td><td>{t3}</td><td>{hy}</td><td>{yr}</td><td class='gt-val'>{g_tot}</td></tr>"
        
        per = (g_tot/m_tot*100) if m_tot > 0 else 0
        
        st.markdown(f"""
        <div class="marksheet-box">
            <div class="school-header"><div class="school-name">{school}</div></div>
            <div class="address">{addr} | Contact: {phone}</div>
            <div class="info-container">
                <div class="info-left">S.R. NO &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {s_data.get('S.R. No','-')}<br>NAME : {s_data.get('Student Name','-')}<br>FATHER : {s_data.get("Father's Name",'-')}<br>MOTHER : {s_data.get("Mother's Name",'-')}</div>
                <div class="info-right">CLASS : {selected_class}<br>D.O.B. : {s_data.get('Date of Birth','-')}<br>EXAM R.N. : {s_data.get('Exam R.N.','-')}<br>GENDER : {s_data.get('Gender','-')}</div>
            </div>
            <table class="marks-table">
                <tr><th>SUBJECT</th><th>MAX</th><th>MIN</th><th>T1</th><th>T2</th><th>T3</th><th>HY</th><th>YR</th><th>TOTAL</th></tr>
                {m_html}
            </table>
            <div class="result-section">
                <span>TOTAL: {g_tot}/{m_tot}</span>
                <span>PERCENTAGE: {per:.2f}%</span>
                <span>DIVISION: <span style="color:blue;">{get_division(per) if not is_failed else 'FAIL'}</span></span>
            </div>
            <div class="footer-sig">
    <div class="sig-box">
        <div class="sig-font">SignCteac</div>
        <div style="border-top: 1px solid #000;">CLASS TEACHER</div>
    </div>
    <div class="sig-box">
        <div class="sig-font">S.Exam.ji</div>
        <div style="border-top: 1px solid #000;">SIGN. EXAM INCHARGE</div>
    </div>
    <div class="sig-box">
        <div class="sig-font">SignPji</div>
        <div style="border-top: 1px solid #000;">PRINCIPAL</div>
    </div>
</div>
	""", unsafe_allow_html=True)
else:
    st.info("💡 डेटा भरें और प्रीव्यू देखें।")