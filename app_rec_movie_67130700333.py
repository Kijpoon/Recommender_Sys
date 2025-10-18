import streamlit as st
import pickle
import pandas as pd
from myfunction_67130700333 import get_movie_recommendations

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="🎬 Smart Movie Recommender",
    page_icon="🎥",
    layout="centered"
)

# ---------- TITLE SECTION ----------
st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'>🎬 Smart Movie Recommender System</h1>
    <p style='text-align: center; color: gray;'>Upload your data → Choose parameters → Get recommendations instantly!</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------- UPLOAD FILE ----------
uploaded_file = st.file_uploader("📂 Upload your recommendation data (.pkl)", type=["pkl"])

if uploaded_file is not None:
    data = pickle.load(uploaded_file)

    user_similarity_df = data.get("user_similarity_df")
    user_movie_ratings = data.get("user_movie_ratings")

    if user_similarity_df is not None and user_movie_ratings is not None:
        st.success("✅ Data successfully loaded!")

        # ---------- PARAMETER SELECTION ----------
        st.markdown("### ⚙️ Choose Parameters")

        col1, col2 = st.columns(2)
        with col1:
            user_id = st.selectbox(
                "Select User ID",
                user_similarity_df.index.tolist(),
                help="Pick a user from your dataset"
            )
        with col2:
            n_recommendations = st.slider(
                "Number of Recommendations",
                min_value=1,
                max_value=20,
                value=5,
                help="Select how many recommendations to generate"
            )

        # Show parameter summary in a table
        param_table = pd.DataFrame({
            "Parameter": ["User ID", "Number of Recommendations"],
            "Value": [user_id, n_recommendations]
        })
        st.markdown("#### 🧾 Current Parameters")
        st.dataframe(param_table, use_container_width=True)

        # ---------- GET RECOMMENDATIONS ----------
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 🎯 Get Personalized Recommendations")

        if st.button("✨ Generate Recommendations"):
            try:
                recommendations = get_movie_recommendations(
                    user_id,
                    user_similarity_df,
                    user_movie_ratings,
                    n_recommendations
                )

                if recommendations:
                    st.success("🎉 Recommendations generated successfully!")
                    st.markdown("### 🍿 Recommended Movies")
                    
                    # Display as cards
                    for idx, movie in enumerate(recommendations, 1):
                        st.markdown(
                            f"""
                            <div style='padding:10px;margin-bottom:10px;
                                background-color:#f7f7f9;
                                border-radius:10px;
                                border-left:5px solid #FF4B4B;'>
                                <b>{idx}. {movie}</b>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.warning("No recommendations found for this user.")
            except Exception as e:
                st.error(f"❌ Error generating recommendations: {e}")

    else:
        st.error("❌ Missing keys: expected 'user_similarity_df' and 'user_movie_ratings'")
else:
    st.info("👆 Please upload your `.pkl` file to begin.")

# ---------- FOOTER ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center; color:gray;'>
    <small>🚀 Built with Streamlit by Poon's Recommendation System</small>
    </div>
    """,
    unsafe_allow_html=True
)
