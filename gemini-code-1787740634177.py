import streamlit as st
import pandas as pd

# ตั้งค่าหน้าตาเว็บ Dashboard
st.set_page_config(page_title="Cookie Run Queue Tracker", page_icon="🎮", layout="wide")

# ปรับแต่ง CSS ตกแต่งให้สวยงาม ดูสะอาดตา
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🎮 ระบบติดตามสถานะเชิญเพื่อน Cookie Run</div>", unsafe_allow_html=True)

# 📌 ใส่ Spreadsheet ID ของคุณตรงนี้
SPREADSHEET_ID = "1vZi4vkxw3hmUjteYVXYLDlhzLgrtLJySny_JiGaLtWc"
SHEET_NAME = "Sheet1"

GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=5) # ดึงข้อมูลใหม่จาก Google Sheets ทุก 5 วินาที
def load_data():
    df = pd.read_csv(GSHEET_URL)
    
    # ดึงคอลัมน์แรกเป็นคอลัมน์ลิงก์
    col_link = df.columns[0]
    
    # ดึงคอลัมน์ที่เหลือทั้งหมดที่เป็นการเก็บสถานะงาน
    status_cols = df.columns[1:]
    
    # ฟังก์ชันนับเครื่องหมาย ✅ ในทุกแถวแบบถูกต้อง
    def count_ticks(row):
        ticks = 0
        for col in status_cols:
            val = str(row[col]).strip()
            if '✅' in val or val == 'TRUE':
                ticks += 1
        return ticks

    df['tick_count'] = df.apply(count_ticks, axis=1)
    return df, col_link

def mask_url(url):
    url_str = str(url).strip()
    if len(url_str) >= 4:
        return url_str[:-4] + "****"
    return url_str

try:
    df, col_link = load_data()
    df['masked_link'] = df[col_link].apply(mask_url)
    
    in_progress_df = df[(df['tick_count'] > 0) & (df['tick_count'] < 3)]
    waiting_df = df[df['tick_count'] == 0]
    completed_df = df[df['tick_count'] >= 3]

    # --- ⚡ 1. คิวที่กำลังทำอยู่ขณะนี้ (ย้ายมาไว้บนสุด) ---
    st.subheader("⚡ คิวที่กำลังทำอยู่ขณะนี้")
    if not in_progress_df.empty:
        for idx, row in in_progress_df.iterrows():
            ticks = row['tick_count']
            done_count = ticks * 10
            progress_pct = min(int((ticks / 3) * 100), 100)
            
            with st.container():
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"🔗 **ลิงก์:** `{row['masked_link']}`")
                    st.progress(progress_pct)
                with col_b:
                    st.success(f"📌 ความคืบหน้า: **{done_count} / 30**")
                st.divider()
    else:
        st.info("💡 ขณะนี้ยังไม่มีคิวที่กำลังรันอยู่ หรือคิวล่าสุดเสร็จเรียบร้อยแล้ว")

    # --- ⌛ 2. คิวที่รอถัดไป ---
    st.subheader("⌛ คิวที่รอถัดไป")
    next_queues = waiting_df.head(5)
    if not next_queues.empty:
        for idx, row in next_queues.iterrows():
            st.warning(f"🔹 **รอทำคิวถัดไป:** `{row['masked_link']}` — 🕒 สถานะ: **รอคิว (0/30)**")
    else:
        st.caption("ไม่มีคิวรอทำในระบบ")

    st.markdown("---")

    # --- 🔍 3. ช่องค้นหาคิวของตนเองสำหรับลูกค้า ---
    st.subheader("🔍 ตรวจสอบสถานะคิวของคุณ")
    search_input = st.text_input("วางลิงก์ของคุณที่นี่เพื่อค้นหาสถานะ:", placeholder="เช่น https://cookierunglobal.onelink.me/...")

    if search_input:
        search_result = df[df[col_link].astype(str).str.contains(search_input.strip(), case=False, na=False)]
        if not search_result.empty:
            for _, row in search_result.iterrows():
                ticks = row['tick_count']
                if ticks >= 3:
                    status_text = "✅ ทำสำเร็จเรียบร้อยแล้ว (30/30)"
                    progress_pct = 100
                elif ticks == 2:
                    status_text = "⏳ กำลังดำเนินการ (20/30)"
                    progress_pct = 66
                elif ticks == 1:
                    status_text = "⏳ กำลังดำเนินการ (10/30)"
                    progress_pct = 33
                else:
                    status_text = "🕒 กำลังรอคิว (0/30)"
                    progress_pct = 0

                st.success(f"🎉 **พบข้อมูลคิวของคุณ!**")
                st.write(f"🔗 ลิงก์: `{row['masked_link']}`")
                st.write(f"📊 สถานะ: **{status_text}**")
                st.progress(progress_pct)
        else:
            st.error("❌ ไม่พบลิงก์นี้ในระบบ กรุณาตรวจสอบลิงก์ใหม่อีกครั้ง")

    st.markdown("---")

    # --- 📊 4. สรุปภาพรวมตัวเลข (ย้ายมาไว้ด้านล่างสุด) ---
    st.subheader("📊 สรุปภาพรวมระบบ")
    m1, m2, m3 = st.columns(3)
    m1.metric("📋 คิวทั้งหมดในระบบ", f"{len(df)} คิว")
    m2.metric("⚡ กำลังดำเนินการ", f"{len(in_progress_df)} คิว")
    m3.metric("✅ ทำเสร็จแล้ว", f"{len(completed_df)} คิว")

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheets: {e}")
