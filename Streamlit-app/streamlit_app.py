import streamlit as st
import requests
import base64

# -------------------------------------------------------------------------------------------------------------------------
                                            # ----- Page Configuration -----#
# -------------------------------------------------------------------------------------------------------------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ----------------------------------------------------------------------------------------------------------------------------
                       # --------- Setting path for protein image to be displayed on the webpage ----------
# ----------------------------------------------------------------------------------------------------------------------------
page_icon = get_base64_of_bin_file("/Protein.jpg")
st.set_page_config(
    page_title="Predicting Clinical Relevance of Missense Mutations with Machine Learning and Protein Structural Information",
    page_icon=f"data:image/jpeg;base64,{page_icon}",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------------------------------------------------------
                                            # ----- Custom CSS Styling -----#
# ----------------------------------------------------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Background color for the app container */
    [data-testid="stAppViewContainer"] {
        background-color: #697da5;
    }
    /* Customize h1 elements */
    h1 {
        color: #333333;
        font-size: 4em;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------------------------------------------------------------
                                         # ----- Display the Image in the Streamlit App Body -----#
                          # -------- Create three columns and place the image in the middle column ---------#
# ----------------------------------------------------------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("./Protein.jpg", caption="Protein Image")

# ----------------------------------------------------------------------------------------------------------------------------
                         # ----------- Backend URL (Render) where the FastAPI server is running ------------#
#-----------------------------------------------------------------------------------------------------------------------------
API_URL = "https://predicting-clinical-relevance-of.onrender.com"

# ----------------------------------------------------------------------------------------------------------------------------
                         # -------------- Set the page tile and description ---------------#
# ----------------------------------------------------------------------------------------------------------------------------
st.title("Predicting Clinical Relevance of Missense Mutations with Machine Learning and Protein Structural Information")
st.write("Enter the feature values to get a prediction:")

# --------------------------------------------------------
   # Retrieve expected feature names from the FastAPI API
# --------------------------------------------------------
try:
    response = requests.get(f"{API_URL}/feature_names")
    response.raise_for_status()
    data = response.json()
    feature_names = data.get("feature_names", [])
except Exception as e:
    st.error(f"Error fetching feature names: {e}")
    feature_names = []

# -----------------------------------------------------------
     # Create input fields for each expected feature
# ----------------------------------------------------------
input_features = {}
if feature_names:
    st.write("Please fill in the values for each feature:")
    for feature in feature_names:
        input_features[feature] = st.number_input(f"{feature}", value=0.0)
    
    if st.button("Predict"):
        payload = {"features": input_features}
        try:
            pred_response = requests.post(f"{API_URL}/predict", json=payload)
            pred_response.raise_for_status()
            result = pred_response.json()
            prediction = result.get("prediction")
            st.success(f"Prediction: {prediction}  (0 = Benign, 1 = Pathogenic)")
        except Exception as e:
            st.error(f"Error during prediction: {e}")
else:
    st.warning("Feature names could not be loaded from the API.")
