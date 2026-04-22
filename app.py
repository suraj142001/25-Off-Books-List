import streamlit as st
import pandas as pd
import urllib.parse
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

# =========================
# CSS
# =========================
st.markdown("""
<style>
body {
    font-family: 'Noto Sans Devanagari', sans-serif;
}
thead tr th {
    background-color: #1f3b73 !important;
    color: white !important;
    text-align: center;
}
tbody tr td {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📚 राजहंस पुस्तक पेठ , पुणे ०३८")
st.subheader("📚 जागतिक पुस्तक दिन ऑफर")

# =========================
# LOAD DATA
# =========================
if not os.path.exists("books_marathi.csv"):
    st.error("CSV file नाही")
    st.stop()

df = pd.read_csv("books_marathi.csv")

# =========================
# SEARCH
# =========================
search = st.text_input("🔍 पुस्तक शोधा")

if search:
    df = df[df["पुस्तकाचे नाव"].str.contains(search, case=False)]

# =========================
# CART INIT
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}

# =========================
# TABLE DISPLAY
# =========================
st.markdown("## 📚 सर्व पुस्तके")

# Display only required columns
display_df = df[[
    "पुस्तकाचे नाव",
    "लेखक",
    "प्रकाशक",
    "किंमत",
    "सवलतीत किंमत"
]]

st.dataframe(
    display_df,
    use_container_width=True,
    height=500   # 👉 scrolling control (increase if needed)
)

# =========================
# QUICK ADD SECTION
# =========================
st.markdown("## ➕ पुस्तक निवडा")

col1, col2 = st.columns([3,1])

with col1:
    selected_book = st.selectbox(
        "पुस्तक निवडा",
        df["पुस्तकाचे नाव"]
    )

with col2:
    qty = st.number_input("Qty", min_value=1, value=1)

if st.button("🛒 Add to Cart"):

    price = df[df["पुस्तकाचे नाव"] == selected_book]["सवलतीत किंमत"].values[0]

    if selected_book not in st.session_state.cart:
        st.session_state.cart[selected_book] = {"qty": 0, "price": price}

    st.session_state.cart[selected_book]["qty"] += qty
    st.success("Cart मध्ये add झाले")

# =========================
# CART
# =========================
st.markdown("## 🛒 Cart")

total = 0
has_items = False

for book, item in st.session_state.cart.items():
    if item["qty"] > 0:
        has_items = True
        amt = item["qty"] * item["price"]
        total += amt
        st.write(f"{book} | Qty: {item['qty']} | ₹{amt}")

if not has_items:
    st.info("Cart रिकामा आहे")

st.markdown(f"### 💰 Total: ₹{total}")

# =========================
# USER INFO
# =========================
name = st.text_input("नाव")
mobile = st.text_input("मोबाईल नंबर")

# =========================
# WHATSAPP ORDER
# =========================
if st.button("🟢 WhatsApp Order"):

    if not has_items:
        st.warning("Cart रिकामा आहे")
    elif not name or not mobile:
        st.warning("माहिती भरा")
    else:
        msg = "नमस्कार 🙏\n\nOrder:\n\n"

        for book, item in st.session_state.cart.items():
            if item["qty"] > 0:
                msg += f"{book} x {item['qty']} = ₹{item['qty']*item['price']}\n"

        msg += f"\nTotal: ₹{total}"
        msg += f"\nName: {name}"
        msg += f"\nMobile: {mobile}"

        url = f"https://wa.me/919322630703?text={urllib.parse.quote(msg)}"
        st.markdown(f"[📲 WhatsApp Order]({url})")

# =========================
# CLEAR CART
# =========================
if st.button("🗑️ Clear Cart"):
    st.session_state.cart = {}
    st.rerun()
