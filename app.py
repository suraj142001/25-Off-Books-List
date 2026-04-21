import streamlit as st
import pandas as pd
import urllib.parse
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Book Store", layout="wide")

# =========================
# CSS + FONT
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600&display=swap');

html, body {
    font-family: 'Noto Sans Devanagari', sans-serif;
}

.stApp {
    background-color: #f5f7fa;
}

.card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1,6])

with col1:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=900)

with col2:
    st.markdown("<h2>📚 राजहंस पुस्तक पेठ , पुणे ०३८</h2>", unsafe_allow_html=True)
    st.markdown("<h2>📚 जागतिक पुस्तक दिन 📚  </h2>", unsafe_allow_html=True)
    st.caption("🎉 ऑफर कालावधी : 23 एप्रिल ते 26 एप्रिल २०२६ पर्यंत")

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

filtered_df = df.copy()
if search:
    filtered_df = filtered_df[
        filtered_df["पुस्तकाचे नाव"].str.contains(search, case=False)
    ]

# =========================
# CART INIT
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}

# =========================
# BOOK GRID
# =========================
st.markdown("## 📚 पुस्तके")

cols = st.columns(3)

for i, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[i % 3]

    book = row["पुस्तकाचे नाव"]
    author = row["लेखक"]  
    publisher = row["प्रकाशक"]
    price = row["किंमत"]
    discount = row["सवलतीत किंमत"]

    with col:
        st.markdown(f"""
        <div class="card">
        <h4>{book}</h4>
        <p>✍️ {author}</p>
        <p>🏢 {publisher}</p>
        <p style="text-decoration: line-through;">₹{price}</p>
        <p style="color:green;font-weight:bold;">₹{discount}</p>
        </div>
        """, unsafe_allow_html=True)

        if book not in st.session_state.cart:
            st.session_state.cart[book] = {"qty": 0, "price": discount}

        c1, c2, c3 = st.columns([1,1,1])

        # ➖
        with c1:
            if st.button("➖", key=f"minus_{i}"):
                if st.session_state.cart[book]["qty"] > 0:
                    st.session_state.cart[book]["qty"] -= 1
                    st.rerun()

        # Qty
        with c2:
            st.markdown(
                f"<h4 style='text-align:center'>{st.session_state.cart[book]['qty']}</h4>",
                unsafe_allow_html=True
            )

        # ➕
        with c3:
            if st.button("➕", key=f"plus_{i}"):
                st.session_state.cart[book]["qty"] += 1
                st.rerun()

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
        st.write(f"📚 {book} | Qty: {item['qty']} | ₹{amt}")

if not has_items:
    st.info("Cart रिकामा आहे")

st.markdown(f"### 💰 Total: ₹{total}")

# =========================
# USER INFO
# =========================
name = st.text_input("नाव")
mobile = st.text_input("मोबाईल नंबर")

# =========================
# WHATSAPP
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
# CLEAR
# =========================
if st.button("🗑️ Clear Cart"):
    st.session_state.cart = {}
    st.rerun()




import requests

def get_book_image(book_name):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{book_name}"
    try:
        res = requests.get(url).json()
        if "items" in res:
            return res["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
    except:
        return None
