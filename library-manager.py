
import streamlit as st
from streamlit_lottie import st_lottie
import json

# ---- Book Animation (embedded JSON) ----
lottie_book = {
    "v": "5.7.6",
    "fr": 30,
    "ip": 0,
    "op": 90,
    "w": 500,
    "h": 500,
    "nm": "book animation",
    "ddd": 0,
    "assets": [],
    "layers": [
        {
            "ddd": 0,
            "ind": 1,
            "ty": 4,
            "nm": "Open Book",
            "sr": 1,
            "ks": {
                "o": {"a": 0, "k": 100},
                "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [250, 250, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "shapes": [
                {
                    "ty": "rect",
                    "nm": "Page",
                    "p": {"a": 0, "k": [0, 0]},
                    "s": {"a": 0, "k": [300, 200]},
                    "r": {"a": 0, "k": 20},
                    "fill": {"a": 0, "k": [0.9, 0.9, 1, 1]}
                }
            ],
            "ao": 0,
            "ip": 0,
            "op": 90,
            "st": 0,
            "bm": 0
        }
    ]
}

# ---- Streamlit Config ----
st.set_page_config(page_title="Library Manager", layout="wide")

# ---- Session State Setup ----
if "books" not in st.session_state:
    st.session_state.books = [
        {"title": "The Alchemist", "author": "Paulo Coelho", "read": True},
        {"title": "1984", "author": "George Orwell"},
        {"title": "Atomic Habits", "author": "James Clear", "read": False}
    ]

# ---- Layout: Left = Animation | Right = Content ----
col1, col2 = st.columns([1, 3])

with col1:
    st_lottie(lottie_book, height=250, key="book")

with col2:
    st.title("Your Books")

    # Show existing books
    for i, book in enumerate(st.session_state.books):
        title = book.get("title", "Untitled")
        author = book.get("author", "Unknown Author")
        read = book.get("read", False)
        status = '✅ Read' if read else '❌ Unread'
        cols = st.columns([5, 1])
        with cols[0]:
            st.markdown(f"*{title}* by {author} — {status}")
        with cols[1]:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.books.pop(i)
                st.experimental_rerun()

    st.markdown("---")

    # Add new book
    with st.expander("➕ Add a new book"):
        new_title = st.text_input("Book Title")
        new_author = st.text_input("Author")
        read_status = st.checkbox("Mark as Read", value=False)
        if st.button("Add Book"):
            if new_title and new_author:
                st.session_state.books.append({
                    "title": new_title,
                    "author": new_author,
                    "read": read_status
                })
                st.success("Book added!")
                st.experimental_rerun()
            else:
                st.warning("Please fill in both title and author.")

# ---- Footer ----
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Made with ❤️ by Kashaf Yasir | Personal Library Manager"
    "</div>",
    unsafe_allow_html=True
)
