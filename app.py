import streamlit as st
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="學校愛校服務系統", layout="centered")
st.title("🏫 愛校服務管理系統")

# 模擬資料庫（實際開發時請串接 Google Sheets 或 Firebase）
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"學號": "112001", "學生姓名": "張小明", "登記日期": "2026-06-01", "時數": 2, "狀態": "待認證"},
        {"學號": "112002", "學生姓名": "李小華", "登記日期": "2026-05-25", "時數": 1, "狀態": "已認證"}
    ])

# 2. 側邊欄切換角色
role = st.sidebar.radio("請選擇操作角色：", ["學生端（查詢與登記）", "老師端（審核與認證）"])

# --- 學生端介面 ---
if role == "學生端（查詢與登記）":
    st.header("🔍 學生服務專區")
    
    # 查詢功能
    search_id = st.text_input("輸入學號查詢時數：")
    if search_id:
        df = st.session_state.db
        result = df[df["學號"] == search_id]
        if not result.empty:
            st.dataframe(result)
            total_hours = result[result["狀態"] == "已認證"]["時數"].sum()
            st.success(f"您目前已完成的有效愛校時數為：{total_hours} 小時")
        else:
            st.warning("查無此學號的紀錄。")
            
    st.divider()
    
    # 登記功能
    st.subheader("📅 預約愛校服務")
    with st.form("register_form"):
        stu_id = st.text_input("學號")
        stu_name = st.text_input("姓名")
        date = st.date_input("預計服務日期")
        hours = st.number_input("預計時數", min_value=1, max_value=4, step=1)
        submitted = st.form_submit_button("送出登記")
        
        if submitted:
            # 這裡寫入資料庫邏輯
            new_data = {"學號": stu_id, "學生姓名": stu_name, "登記日期": str(date), "時數": hours, "狀態": "待認證"}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
            st.success("登記成功！請準時出席並請老師認證。")

# --- 老師端介面 ---
elif role == "老師端（審核與認證）":
    st.header("👨‍🏫 老師審核專區")
    
    # 簡單的密碼驗證（防學生誤入）
    password = st.text_input("請輸入教師認證密碼：", type="password")
    if password == "school1234": # 實際應用請用安全的方式處理
        st.write("目前待審核的預約名單：")
        df = st.session_state.db
        
        # 顯示待認證資料
        pending_df = df[df["狀態"] == "待認證"]
        st.dataframe(pending_df)
        
        # 審核操作
        if not pending_df.empty:
            student_to_approve = st.selectbox("請選擇要認證的學生學號：", pending_df["學號"].unique())
            if st.button("確認該生已完成愛校（通過認證）"):
                # 更新資料狀態
                st.session_state.db.loc[st.session_state.db["學號"] == student_to_approve, "狀態"] = "已認證"
                st.success(f"學號 {student_to_approve} 已成功認證！")
                st.rerun()
    elif password:
        st.error("密碼錯誤！")