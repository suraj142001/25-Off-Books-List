import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Book Store", layout="wide")

# =========================
# CSS (Amazon Style)
# =========================
st.markdown("""
<style>
body {
    background-color: #eaeded;
}

.navbar {
    background-color: #131921;
    padding: 10px;
    color: white;
    font-size: 22px;
    font-weight: bold;
}

.card {
    background-color: white;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #ddd;
    transition: 0.2s;
    height: 100%;
}

.card:hover {
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
}

.price {
    color: #B12704;
    font-size: 18px;
    font-weight: bold;
}

.oldprice {
    text-decoration: line-through;
    color: gray;
}

button[kind="primary"] {
    background-color: #FFD814;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
st.markdown('<div class="navbar">📚 Book Store</div>', unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("books_with_images.csv")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

search = st.sidebar.text_input("Search Book")

authors = st.sidebar.multiselect(
    "Author", options=df["लेखक"].unique()
)

publishers = st.sidebar.multiselect(
    "Publisher", options=df["प्रकाशक"].unique()
)

# =========================
# FILTER LOGIC
# =========================
filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["पुस्तकाचे नाव"].str.contains(search, case=False)
    ]

if authors:
    filtered_df = filtered_df[
        filtered_df["लेखक"].isin(authors)
    ]

if publishers:
    filtered_df = filtered_df[
        filtered_df["प्रकाशक"].isin(publishers)
    ]

# =========================
# CART
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}

# =========================
# PRODUCTS GRID
# =========================
st.markdown("## 🛍️ Books")

cols = st.columns(4)

for i, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[i % 4]

    book = row["पुस्तकाचे नाव"]
    price = row["किंमत"]
    discount = row["सवलतीत किंमत"]
    img = row.get("image_url", "")

    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if img:
            st.image(img, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/150")

        st.markdown(f"**{book}**")
        st.markdown(f"<span class='oldprice'>₹{price}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='price'>₹{discount}</div>", unsafe_allow_html=True)

        if st.button("🛒 Add to Cart", key=f"cart_{i}"):
            if book not in st.session_state.cart:
                st.session_state.cart[book] = 0
            st.session_state.cart[book] += 1

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# CART SIDEBAR
# =========================
st.sidebar.header("🛒 Cart")

total = 0

for book, qty in st.session_state.cart.items():
    price = df[df["पुस्तकाचे नाव"] == book]["सवलतीत किंमत"].values[0]
    amt = qty * price
    total += amt
    st.sidebar.write(f"{book} x {qty} = ₹{amt}")

st.sidebar.markdown(f"### Total: ₹{total}")

if st.sidebar.button("Clear Cart"):
    st.session_state.cart = {}
    st.rerun()
