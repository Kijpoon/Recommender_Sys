import streamlit as st
import pandas as pd
import pickle
from myfunction_67130700333 import get_movie_recommendations

# --- Page Configuration ---
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎥",
    layout="centered"
)

# --- Load Data ---
@st.cache_data(show_spinner=False)
def load_data():
    """Load precomputed recommendation data."""
    with open("recommendation_data.pkl", "rb") as f:
        user_similarity_df, user_movie_ratings = pickle.load(f)
    return user_similarity_df, user_movie_ratings


# --- Main UI ---
st.title("🎬 Movie Recommendation System")
st.markdown(
    """
    Welcome to the **Movie Recommender** app!  
    Enter your user ID to get personalized movie suggestions  
    based on your viewing similarity with other users.
    """
)

try:
    user_similarity_df, user_movie_ratings = load_data()

    max_user_id = int(user_movie_ratings.index.max())

    user_id = st.number_input(
        "Enter a User ID:",
        min_value=1,
        max_value=max_user_id,
        value=1,
        step=1
    )

    if st.button("🎯 Get Recommendations"):
        with st.spinner("Finding your best matches..."):
            try:
                recommendations = get_movie_recommendations(
                    user_id=user_id,
                    user_similarity_df=user_similarity_df,
                    user_movie_ratings=user_movie_ratings,
                    top_n=10
                )

                if recommendations:
                    st.success(f"Top 10 movie recommendations for User {user_id}:")
                    st.write("")  # spacing
                    for i, movie in enumerate(recommendations, start=1):
                        st.markdown(f"**{i}. {movie}** 🎞️")
                else:
                    st.warning("No recommendations available for this user yet.")

            except Exception as e:
                st.error(f"⚠️ Error during recommendation: {e}")

except FileNotFoundError:
    st.error("❌ Data file `recommendation_data.pkl` not found.")
    st.info("Please ensure the file exists in the same directory as this script.")
except ImportError:
    st.error("❌ Function file `myfunction_67130700333.py` not found.")
    st.info("Please ensure your function script is uploaded.")
