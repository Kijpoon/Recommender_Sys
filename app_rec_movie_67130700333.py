import streamlit as st
import pickle
import pandas as pd
from myfunction_67130700333 import get_movie_recommendations

st.set_page_config(page_title="🎬 Movie Recommendation App", layout="centered")

st.title("🎥 Movie Recommendation System")
st.markdown("Upload your data file and choose parameters to get personalized recommendations.")

# --- Step 1: Upload the pickle data file ---
uploaded_file = st.file_uploader("📂 Upload Recommendation Data (.pkl)", type=["pkl"])

if uploaded_file is not None:
    data = pickle.load(uploaded_file)
    
    # Expect the file to contain required dataframes
    user_similarity_df = data.get("user_similarity_df")
    user_movie_ratings = data.get("user_movie_ratings")

    if user_similarity_df is not None and user_movie_ratings is not None:
        st.success("✅ Data successfully loaded!")

        # --- Step 2: Choose user and parameters ---
        st.subheader("⚙️ Choose Parameters")
        user_id = st.selectbox("Select User ID:", user_similarity_df.index.tolist())
        n_recommendations = st.slider("Number of recommendations:", 1, 20, 5)

        # Show parameter table
        param_table = pd.DataFrame({
            "Parameter": ["User ID", "Number of Recommendations"],
            "Value": [user_id, n_recommendations]
        })
        st.table(param_table)

        # --- Step 3: Get Recommendations ---
        if st.button("🎯 Get Recommendations"):
            try:
                recommendations = get_movie_recommendations(
                    user_id, user_similarity_df, user_movie_ratings, n_recommendations
                )

                if recommendations:
                    st.success("✅ Recommendations generated!")
                    st.write("### 🍿 Recommended Movies:")
                    st.write(pd.DataFrame({"Movie": recommendations}))
                else:
                    st.warning("No recommendations found for this user.")
            except Exception as e:
                st.error(f"Error generating recommendations: {e}")
    else:
        st.error("❌ Missing expected keys in your .pkl file: 'user_similarity_df' or 'user_movie_ratings'")
else:
    st.info("👆 Please upload your `.pkl` file to begin.")
