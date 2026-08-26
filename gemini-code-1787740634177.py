import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cookie Run Queue Tracker", page_icon="🎮", layout="wide")

st.title("🎮 ระบบติดตามคิวทำกิจกรรม Cookie Run")

# 📌 1. ใส่ Spreadsheet ID ของคุณตรงนี้
# (เช่น จากลิงก์ https://docs.google.com/spreadsheets/d/1ABC123xxxx/edit ให้เอาแค่ส่วน 1ABC123xxxx)
SPREADSHEET_ID = "1vZi4vkxw3hmUjteYVXYLDlhzLgrtLJySny_JiGaLtWc"
SHEET_NAME = "Sheet1" # ชื่อแท็บใน Google Sheets

# ดึงข้อมูลจาก Google Sheets ออกมาเป็น CSV Format
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=10) # 🔄 ดึงข้อมูลใหม่จาก Google Sheets ทุกๆ 10 วินาที
def load_data():
    df = pd.read_csv(GSHEET_URL)
    status_cols = [c for c in df.columns if 'สถานะงาน' in c]
    # นับจำนวนเครื่องหมาย ✅
    df['tick_count'] = df[status_cols].apply(lambda row: sum(1 for v in row if str(v).strip() == '✅'), axis=1)
    return df

def mask_url(url):
    url_str = str(url).strip()
    return url_str[:-4] + "****" if len(url_str) >= 4 else url_str

try:
    df = load_data()
    col_link = df.columns[0]
    df['masked_link'] = df[col_link].apply(mask_url)
    
    # แยกกลุ่มคิวงาน
    completed_df = df[df['tick_count'] >= 3]
    in_progress_df = df[(df['tick_count'] > 0) & (df['tick_count'] < 3)]
    waiting_df = df[df['tick_count'] == 0]

    # --- 1. คิวรอทำ (แสดงแค่ 2 คิวแรก) ---
    st.subheader("⌛ คิวรอทำ (2 คิวถัดไป)")
    next_queues = waiting_df.head(2)
    if not next_queues.empty:
        for idx, row in next_queues.iterrows():
            st.warning(f"🔹 **คิวรอทำ:** `{row['masked_link']}` | **สถานะ:** 🕒 กำลังรอคิว (0/30)")
    else:
        st.info("ไม่มีคิวค้าง หรือทุกคิวดำเนินการไปแล้ว")

    st.markdown("---")

    # --- 2. ภาพรวมสถานะ ---
    col1, col2, col3 = st.columns(3)
    col1.metric("คิวทั้งหมด", len(df))
    col2.metric("กำลังทำ", len(in_progress_df))
    col3.metric("สำเร็จแล้ว", len(completed_df))

    st.markdown("---")

    # --- 3. ค้นหาคิว ---
    st.subheader("🔍 ค้นหาคิวของคุณ")
    search_query = st.text_input("กรอกลิงก์บางส่วนเพื่อค้นหา:")
    
    display_df = df.copy()
    if search_query:
        display_df = display_df[display_df[col_link].astype(str).str.contains(search_query, case=False, na=False)]

    for idx, row in display_df.iterrows():
        ticks = row['tick_count']
        if ticks >= 3:
            status_text = "✅ สำเร็จแล้ว (30/30)"
            progress_pct = 100
        elif ticks == 2:
            status_text = "⏳ ดำเนินการแล้ว (20/30)"
            progress_pct = 66
        elif ticks == 1:
            status_text = "⏳ ดำเนินการแล้ว (10/30)"
            progress_pct = 33
        else:
            status_text = "🕒 กำลังรอคิว (0/30)"
            progress_pct = 0

        with st.container():
            c1, c2, c3 = st.columns([3, 2, 2])
            c1.write(f"🔗 **คิวที่ {idx+1}:** `{row['masked_link']}`")
            c2.write(f"**สถานะ:** {status_text}")
            c3.progress(progress_pct)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheets: {e}")