import streamlit as st
import pandas as pd

# =========================================================
# ตั้งค่าหน้าตาเว็บ Dashboard
# =========================================================
st.set_page_config(
    page_title="Cookie Run Queue Tracker",
    page_icon="🎮",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #555555;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# หัวเว็บ
# =========================================================
st.markdown(
    "<div class='main-title'>🎮 ดูสถานะคิวเชิญเพื่อน Cookie Run</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>"
    "เป็นงานกดมือ 100% เว็บไซต์นี้มีไว้สำหรับอัพเดตสถานะคิวของท่าน เท่านั้น!!"
    "</div>",
    unsafe_allow_html=True
)

# =========================================================
# Google Sheets
# =========================================================
SPREADSHEET_ID = "1vZi4vkxw3hmUjteYVXYLDlhzLgrtLJySny_JiGaLtWc"
SHEET_NAME = "Sheet1"

GSHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
)

# =========================================================
# โหลดข้อมูล
# =========================================================
@st.cache_data(ttl=5)
def load_data():

    df = pd.read_csv(GSHEET_URL)

    # คอลัมน์แรก = ลิงก์
    col_link = df.columns[0]

    # คอลัมน์สถานะทั้งหมด
    status_cols = df.columns[1:]

    # -----------------------------------------------------
    # ตรวจสอบสถานะของแต่ละแถว
    # -----------------------------------------------------
    def analyze_status(row):

        tick_count = 0
        has_waiting = False

        for col in status_cols:

            val = str(row[col]).strip().upper()

            # มี ⏳ = กำลังทำ
            if "⏳" in val:
                has_waiting = True

            # รองรับเครื่องหมายสำเร็จ
            if "✅" in val or val == "TRUE":
                tick_count += 1

        return pd.Series({
            "tick_count": tick_count,
            "has_waiting": has_waiting
        })

    status_result = df.apply(analyze_status, axis=1)

    df["tick_count"] = status_result["tick_count"]
    df["has_waiting"] = status_result["has_waiting"]

    # -----------------------------------------------------
    # กำหนดสถานะ
    # -----------------------------------------------------
    def get_status(row):

        # ถ้ามี ⏳ อย่างน้อย 1 ช่อง = กำลังทำ
        if row["has_waiting"]:
            return "กำลังทำ"

        # ครบ 3 ช่อง = สำเร็จ
        elif row["tick_count"] >= 3:
            return "สำเร็จ"

        # นอกนั้น = รอคิว
        else:
            return "รอคิว"

    df["status"] = df.apply(get_status, axis=1)

    return df, col_link


# =========================================================
# ปิดบังลิงก์
# =========================================================
def mask_url(url):

    url_str = str(url).strip()

    if len(url_str) >= 4:
        return url_str[:-4] + "**"

    return url_str


# =========================================================
# เริ่มระบบ
# =========================================================
try:

    df, col_link = load_data()

    # สร้างลิงก์แบบปิดท้าย
    df["masked_link"] = df[col_link].apply(mask_url)

    # =====================================================
    # แยกประเภทคิว
    # =====================================================

    # กำลังทำ
    in_progress_df = df[df["status"] == "กำลังทำ"]

    # รอคิว
    waiting_df = df[df["status"] == "รอคิว"]

    # สำเร็จ
    completed_df = df[df["status"] == "สำเร็จ"]

    # =====================================================
    # 1. คิวที่กำลังทำอยู่
    # =====================================================
    st.subheader("⚡ คิวที่กำลังทำอยู่ขณะนี้")

    if not in_progress_df.empty:

        for idx, row in in_progress_df.iterrows():

            ticks = int(row["tick_count"])

            # คำนวณความคืบหน้า
            done_count = min(ticks * 10, 29)

            progress_pct = min(
                int((done_count / 29) * 100),
                100
            )

            with st.container():

                col_a, col_b = st.columns([2, 1])

                with col_a:

                    st.markdown(
                        f"🔗 **ลิงก์:** `{row['masked_link']}`"
                    )

                    st.progress(progress_pct)

                with col_b:

                    st.info(
                        f"⏳ **กำลังทำ** "
                        f"({done_count} / 29)"
                    )

                st.divider()

    else:

        st.info(
            "💡 ขณะนี้ยังไม่มีคิวที่กำลังทำอยู่"
        )

    # =====================================================
    # 2. คิวที่รอถัดไป
    # =====================================================
    st.subheader("⌛ คิวที่รอถัดไป")

    next_queues = waiting_df.head(5)

    if not next_queues.empty:

        for idx, row in next_queues.iterrows():

            st.warning(
                f"🔹 **รอทำคิวถัดไป:** "
                f"`{row['masked_link']}` "
                f"— 🕒 สถานะ: **รอคิว (0/29)**"
            )

    else:

        st.caption(
            "ไม่มีคิวรอทำในระบบ"
        )

    st.markdown("---")

    # =====================================================
    # 3. คิวที่ทำสำเร็จล่าสุด
    # =====================================================
    st.subheader("✅ คิวที่ทำสำเร็จเรียบร้อยแล้ว ล่าสุด")

    if not completed_df.empty:

        # เอา 10 คิวล่าสุด
        latest_completed = completed_df.tail(10).iloc[::-1]

        for idx, row in latest_completed.iterrows():

            st.success(
                f"✅ `{row['masked_link']}` "
                f"— **ทำสำเร็จเรียบร้อยแล้ว (29/29)**"
            )

    else:

        st.caption(
            "ยังไม่มีคิวที่ทำสำเร็จ"
        )

    st.markdown("---")

    # =====================================================
    # 4. ค้นหาคิวของตัวเอง
    # =====================================================
    st.subheader("🔍 ตรวจสอบสถานะคิวของคุณ")

    search_input = st.text_input(
        "วางลิงก์ของคุณที่นี่เพื่อค้นหาสถานะ:",
        placeholder="เช่น https://cookierunglobal.onelink.me/..."
    )

    if search_input:

        search_text = search_input.strip()

        search_result = df[
            df[col_link]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        if not search_result.empty:

            for _, row in search_result.iterrows():

                ticks = int(row["tick_count"])

                # =========================================
                # สำเร็จ
                # =========================================
                if row["status"] == "สำเร็จ":

                    status_text = (
                        "✅ ทำสำเร็จเรียบร้อยแล้ว (29/29)"
                    )

                    progress_pct = 100

                    st.success(
                        "🎉 **พบข้อมูลคิวของคุณ!**"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

                # =========================================
                # กำลังทำ
                # =========================================
                elif row["status"] == "กำลังทำ":

                    done_count = min(
                        ticks * 10,
                        29
                    )

                    progress_pct = min(
                        int((done_count / 29) * 100),
                        100
                    )

                    status_text = (
                        f"⏳ กำลังดำเนินการ "
                        f"({done_count}/29)"
                    )

                    st.info(
                        "🎉 **พบข้อมูลคิวของคุณ!**"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

                # =========================================
                # รอคิว
                # =========================================
                else:

                    status_text = (
                        "🕒 รอทำคิวถัดไป (0/29)"
                    )

                    progress_pct = 0

                    st.warning(
                        "🎉 **พบข้อมูลคิวของคุณ!**"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

        else:

            st.error(
                "❌ ไม่พบลิงก์นี้ในระบบ "
                "กรุณาตรวจสอบลิงก์ใหม่อีกครั้ง"
            )

    st.markdown("---")

    # =====================================================
    # อัปเดตอัตโนมัติ
    # =====================================================
    st.caption(
        "🔄 ระบบอัปเดตข้อมูลจาก Google Sheets ทุก 5 วินาที"
    )


except Exception as e:

    st.error(
        f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheets: {e}"
    )

อยากให้ตกแต่งหน้าตาให้ออกมาสวยงามดูทันสมัยกว่านี้ได้หรือไม่
