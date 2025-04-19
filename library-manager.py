import streamlit as st
import json
import os
from streamlit_lottie import st_lottie
import requests

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_book = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_xlkxtmul.json")

# Load or initialize book data
if os.path.exists("library.json"):
    with open("library.json", "r") as f:
        books = json.load(f)
else:
    books = []

# Page config and styling
st.set_page_config(page_title="Library Manager", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .main {
        background-color: #121212;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    .stTextInput>div>div>input {
        background-color: #1E1E2F;
        color: white;
    }
    .book-card {
        background-color: #1E1E2F;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Personal Library Manager")
st_lottie(lottie_book, height=150)

menu = st.sidebar.radio("Menu", ["View Books", "Add Book", "Search Book", "Statistics"])

# Save function
def save_books():
    with open("library.json", "w") as f:
        json.dump(books, f, indent=4)

# View Books
if menu == "View Books":
    st.subheader("Your Books")
    if not books:
        st.info("No books added yet.")
    for book in books:
        with st.container():
            st.markdown(f"""
                <div class="book-card">
                    <strong>{book['title']}</strong><br>
                    Author: {book['author']}<br>
                    Status: {'✅ Read' if book['read'] else '❌ Unread'}
                </div>
            """, unsafe_allow_html=True)

# Add Book
elif menu == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    read = st.checkbox("Read")

    if st.button("Add Book"):
        if title and author:
            books.append({"title": title, "author": author, "read": read})
            save_books()
            st.success("Book added successfully!")
        else:
            st.warning("Please fill in all fields.")

# Search Book
elif menu == "Search Book":
    st.subheader("Search Books")
    query = st.text_input("Enter book title or author")
    results = [book for book in books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

    if query:
        if results:
            for book in results:
                with st.container():
                    st.markdown(f"""
                        <div class="book-card">
                            <strong>{book['title']}</strong><br>
                            Author: {book['author']}<br>
                            Status: {'✅ Read' if book['read'] else '❌ Unread'}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No matching books found.")

# Stats
elif menu == "Statistics":
    st.subheader("Library Stats")
    total = len(books)
    read = sum(1 for b in books if b["read"])
    unread = total - read

    st.markdown(f"*Total Books:* {total}")
    st.markdown(f"*Read:* {read}")
    st.markdown(f"*Unread:* {unread}")
