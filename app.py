import streamlit as st
import pandas as pd
import pickle
import math
from sklearn.metrics.pairwise import cosine_similarity


# Load the DataFrame from the pickle file
with open('top_50_books_df.pkl', 'rb') as f:
    top_50 = pickle.load(f)

# Define the layout of the app
st.set_page_config(page_title='Top 50 Books', page_icon=':books:', layout='wide')


def top_50_page():
    st.title('Top 50 Books')
    st.write('Here are the top 50 books based on their ratings and popularity:')

    # Calculate the number of rows and columns needed to display all the books
    num_books = top_50.shape[0]
    num_cols = 5
    num_rows = math.ceil(num_books / num_cols)

    # Display the books in rows of 5
    for i in range(num_rows):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            idx = i * num_cols + j
            if idx < num_books:
                with cols[j].container():
                    st.image(top_50.iloc[idx]['Image-URL-M'], width=100)
                    st.write(f"<h3>{idx + 1}. {top_50.iloc[idx]['Book-Title']}</h3>", unsafe_allow_html=True)
                    st.write(f"<p style='font-size:0.9em; margin-bottom: 5px;'>{top_50.iloc[idx]['Book-Author']}</p>",
                             unsafe_allow_html=True)
                    st.write(f"<p style='font-size:0.9em; margin-bottom: 5px;'>ISBN: {top_50.iloc[idx]['ISBN']}</p>",
                             unsafe_allow_html=True)
                    st.write(
                        f"<p style='font-size:0.9em; margin-bottom: 5px;'>Publisher: {top_50.iloc[idx]['Publisher']}</p>",
                        unsafe_allow_html=True)
                    st.write(
                        f"<p style='font-size:0.9em; margin-bottom: 5px;'>Avg Rating: {top_50.iloc[idx]['avg_rating']:.2f}</p>",
                        unsafe_allow_html=True)
                    st.write(
                        f"<p style='font-size:0.9em; margin-bottom: 5px;'>Num Ratings: {top_50.iloc[idx]['num_rating']}</p>",
                        unsafe_allow_html=True)
                    st.markdown(
                        """<style>.stContainer .stMarkdown h3 {margin-bottom: 0.5rem;} .stContainer .stMarkdown p {margin: 0;}</style>""",
                        unsafe_allow_html=True)
                    st.markdown(
                        """<style>.stContainer .stMarkdown {padding: 10px; border-radius: 5px; background-color: #f9f9f9;}</style>""",
                        unsafe_allow_html=True)

def other_recommendations_page():
    st.title('Other Recommendations')

    # Load the pivot table from the pickle file
    with open('pivot_table_df.pkl', 'rb') as f:
        pivot_table = pickle.load(f)

    # Load the pre-pivot dataframe from the pickle file
    with open('pre_pivot.pkl', 'rb') as f:
        pre_pivot_df = pickle.load(f)

    # Get a list of all book titles for the dropdown
    book_titles = list(pivot_table.index)

    # Create a dropdown to select a book
    selected_book = st.selectbox('Select a book:', book_titles)

    # Find the cosine similarities for the selected book
    similarities = cosine_similarity(pivot_table.loc[selected_book].values.reshape(1, -1), pivot_table.values)

    # Get the indices of the top 10 similar books
    similar_book_indices = similarities.argsort()[0][-11:-1][::-1]

    # Display the top 9 similar books
    st.write(f"Here are 9 books similar to {selected_book}:")
    for i, idx in enumerate(similar_book_indices):
        if i == 0:
            continue
        book_title = pivot_table.index[idx]
        book_author = pre_pivot_df.loc[pre_pivot_df['Book-Title']==book_title]['Book-Author'].values[0]
        st.write(f"{i}. {book_title} by {book_author}")


# Create a list of page names and their corresponding functions
PAGES = {
    "Top 50 Books": top_50_page,
    "Other Recommendations": other_recommendations_page,
}

# Create a multiselect widget to select the page to view
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Execute the selected page function
page = PAGES[selection]
page()
