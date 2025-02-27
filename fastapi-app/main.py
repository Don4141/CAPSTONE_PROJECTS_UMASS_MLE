import os
import pickle
import joblib
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras import Model, Sequential, optimizers
from tensorflow.keras.layers import Dense
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import xgboost as xgb
import uvicorn

# --------------------------------------------------------------------
                          # Configure logging
# --------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
                   # Define the AutoEncoder model
# ---------------------------------------------------------------------
class AutoEncoders(tf.keras.Model):
    def __init__(self, input_dim, output_units, **kwargs):
        super().__init__(**kwargs)
        self.input_dim = input_dim
        self.output_units = output_units

        self.encoder = tf.keras.Sequential(
            [
                tf.keras.Input(shape=(input_dim,)),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dense(16, activation="relu")
            ],
            name="encoder"
        )
        self.decoder = tf.keras.Sequential(
            [
                tf.keras.layers.Dense(16, activation="relu"),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dense(output_units, activation="sigmoid")
            ]
        )

    def call(self, inputs, training=None, mask=None):
        encoded = self.encoder(inputs)
        decoded = self.decoder(encoded)
        return decoded

    def get_config(self):
        config = super().get_config()
        config.update({
             "input_dim": self.input_dim,
             "output_units": self.output_units,
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)

# ----------------------------------------------------------------------------
       # File paths for saved models and objects (committed to GitHub)
# ---------------------------------------------------------------------------
AUTOENCODER_PATH = "./autoencoder.keras"
SCALER_PATH = "./scaler.pkl"
XGB_MODEL_PATH = "./xgb_model.pkl"
FEATURE_NAMES_PATH = "./feature_names.pkl"
COLS_TO_DROP_PATH = "./cols_to_drop.pkl"

# ----------------------------------------------------------------------------
                             # Create FastAPI app
# ----------------------------------------------------------------------------
app = FastAPI(title="Clinical Relevance of Missense Mutations Prediction API")

# ----------------------------------------------------------------------------
            # Train the pipeline and save models if not present
# ----------------------------------------------------------------------------
def train_pipeline():
    logger.info("Saved models not found. Running training pipeline...")

    # ---------------------------------------------------------------------------
            # Files are saved in a folder called "data" in my github repo
            # Script is saved in a folder called Web_App in my github repo
    # ---------------------------------------------------------------------------
    TrainBenign_df = pd.read_csv("./data/TrainBenign.csv")
    TrainPathogenic_df = pd.read_csv("./data/TrainPathogenic.csv")
    TestBenign_df = pd.read_csv("./data/TestBenign.csv")
    TestPathogenic_df = pd.read_csv("./data/TestPathogenic.csv")

    # ---------------------------------------------------------------------
                    # Drop rows with missing values
    # ---------------------------------------------------------------------
    TrainBenign_df = TrainBenign_df.dropna(how="any")
    TrainPathogenic_df = TrainPathogenic_df.dropna(how="any")
    TestBenign_df = TestBenign_df.dropna(how="any")
    TestPathogenic_df = TestPathogenic_df.dropna(how="any")
     # -------------------------------------------------------------------
                # List of columns to drop
     # -------------------------------------------------------------------
    col_to_drop = [
        'Pdb', 'Mutation', 'Variant',
        'sloop_entropy', 'mloop_entropy', 'Water_bridge',
        'Electrostatic_kon', 'Partial_covalent_bonds', 'Entropy_Complex',
        'dShort_Loop_Entropy', 'dMedium_Loop_Entropy', 'dWater_Bridge',
        'dElectrostatic_kon', 'dPartial_Covalent_Bonds', 'dEntropy_Complex'
    ]

    # ----------------------------------------------------------------------
                              # Drop the defined columns
    # ----------------------------------------------------------------------
    TrainBenign_df = TrainBenign_df.drop(columns=col_to_drop)
    TrainPathogenic_df = TrainPathogenic_df.drop(columns=col_to_drop)
    TestBenign_df = TestBenign_df.drop(columns=col_to_drop)
    TestPathogenic_df = TestPathogenic_df.drop(columns=col_to_drop)

    # ----------------------------------------------------------------------
                              # Merge and shuffle data
    # ----------------------------------------------------------------------
    train_df = [TrainBenign_df, TrainPathogenic_df]
    test_df = [TestBenign_df, TestPathogenic_df]
    train = pd.concat(train_df).sample(frac=1).reset_index(drop=True)
    test = pd.concat(test_df).sample(frac=1).reset_index(drop=True)

    # ----------------------------------------------------------------------
            # Encode target labels: "Pathogenic" as 1, "Benign" as 0
    # ----------------------------------------------------------------------
    train["Class"] = np.where(train["Class"] == "Pathogenic", 1, 0)
    test["Class"] = np.where(test["Class"] == "Pathogenic", 1, 0)
    
    # ----------------------------------------------------------------------
                        # Split features and target
    # ----------------------------------------------------------------------
    X_train, y_train = train.drop(columns="Class"), train["Class"]
    X_test, y_test = test.drop(columns="Class"), test["Class"]

    # ----------------------------------------------------------------------
                # Save original feature names for later use
    # ----------------------------------------------------------------------
    feature_names = list(X_train.columns)

    # ----------------------------------------------------------------------
                           # Scale the Data #
    # ----------------------------------------------------------------------
    scaler = StandardScaler()
    scaled_X_train = scaler.fit_transform(X_train)
    scaled_X_test = scaler.transform(X_test)

    # ---------------------------------------------------------------------
                           # Build and Train the AutoEncoder #
    # ---------------------------------------------------------------------
    input_dim = scaled_X_train.shape[1]
    auto_encoder = AutoEncoders(input_dim=input_dim, output_units=input_dim)
    optimizer = optimizers.Adam(learning_rate=0.005)
    auto_encoder.compile(loss='mae', metrics=['mae'], optimizer=optimizer)
    logger.info("Training autoencoder...")
    auto_encoder.fit(
        scaled_X_train, 
        scaled_X_train, 
        epochs=50, 
        batch_size=32, 
        validation_data=(scaled_X_test, scaled_X_test),
        verbose=1
    )

     # --------------------------------------------------------------------
                          # Save the trained autoencoder #
     # --------------------------------------------------------------------
    auto_encoder.save(AUTOENCODER_PATH)
    logger.info(f"Autoencoder saved to {AUTOENCODER_PATH}")

    # ---------------------------------------------------------------------
                          # Reduce Feature Dimensions Using the Encoder
    # ---------------------------------------------------------------------
    encoder_layer = auto_encoder.get_layer("encoder")
    reduced_train = pd.DataFrame(encoder_layer.predict(scaled_X_train))
    reduced_train = reduced_train.add_prefix('feature_')
    reduced_test = pd.DataFrame(encoder_layer.predict(scaled_X_test))
    reduced_test = reduced_test.add_prefix('feature_')
    
    # --------------------------------------------------------------------
                          # Identify columns with 1 or 2 unique values
    # --------------------------------------------------------------------
    def show_single_uniq_col(df):
        return [col for col in df.columns if df[col].nunique() in (1, 2)]
    low_variance_cols = show_single_uniq_col(reduced_train)
    logger.info(f"Columns dropped due to low variance: {low_variance_cols}")

    X_train_reduced = reduced_train.drop(columns=low_variance_cols)
    X_test_reduced = reduced_test.drop(columns=low_variance_cols)

    # --------------------------------------------------------------------
                          # Train the XGBoost Classifier
    # --------------------------------------------------------------------
    xgb_clf = xgb.XGBClassifier(
        objective='binary:logistic', 
        n_estimators=500, 
        eta=0.15,
        max_depth=12,
        eval_metric="error",
        early_stopping_rounds=10, 
        random_state=42,
        use_label_encoder=False
    )
    logger.info("Training XGBoost classifier...")
    xgb_clf.fit(X_train_reduced, 
                y_train, eval_set=[(X_test_reduced, y_test)], 
                verbose=False)

    # ---------------------------------------------------------------------
                         # Save the XGBoost model
    # ---------------------------------------------------------------------
    joblib.dump(xgb_clf, XGB_MODEL_PATH)
    logger.info(f"XGBoost model saved to {XGB_MODEL_PATH}")

    # ---------------------------------------------------------------------
                         # Save scaler, feature names, low variance columns
    # ---------------------------------------------------------------------
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)
    with open(FEATURE_NAMES_PATH, "wb") as f:
        pickle.dump(feature_names, f)
    with open(COLS_TO_DROP_PATH, "wb") as f:
        pickle.dump(low_variance_cols, f)
    # --------------------------------------------------------------------
                         # Return all trained objects for further use
    # --------------------------------------------------------------------
    return scaler, auto_encoder, xgb_clf, feature_names, low_variance_cols

# ------------------------------------------------------------------------
    # Load pre-trained objects if they exist, otherwise run train pipeline
# ------------------------------------------------------------------------
if os.path.exists(AUTOENCODER_PATH) and os.path.exists(SCALER_PATH) and \
   os.path.exists(XGB_MODEL_PATH) and os.path.exists(FEATURE_NAMES_PATH) and \
   os.path.exists(COLS_TO_DROP_PATH):
    logger.info("Loading pre-trained models from GitHub repository files...")
    auto_encoder = tf.keras.models.load_model(AUTOENCODER_PATH, custom_objects={"AutoEncoders": AutoEncoders})
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
    xgb_clf = joblib.load(XGB_MODEL_PATH)
    with open(FEATURE_NAMES_PATH, "rb") as f:
        feature_names = pickle.load(f)
    with open(COLS_TO_DROP_PATH, "rb") as f:
        cols_to_drop = pickle.load(f)
else:
    scaler, auto_encoder, xgb_clf, feature_names, cols_to_drop = train_pipeline()
# -------------------------------------------------------------------------
                          # Extract the encoder layer for prediction use
# ------------------------------------------------------------------------
encoder_layer = auto_encoder.get_layer("encoder")

# -------------------------------------------------------------------------
                          # Define the API model and endpoints
# ------------------------------------------------------------------------
class PredictionInput(BaseModel):
    features: Dict[str, float]

@app.get("/feature_names")
def get_feature_names():
    return {"feature_names": feature_names}

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        ordered_features = [input_data.features[name] for name in feature_names]
    except KeyError as e:
        return {"error": f"Missing feature: {e}"}
    
    input_df = pd.DataFrame([ordered_features], columns=feature_names)
    scaled_input = scaler.transform(input_df)
    encoded_input = encoder_layer.predict(scaled_input)
    encoded_df = pd.DataFrame(encoded_input, columns=[f"feature_{i}" for i in range(encoded_input.shape[1])])
    reduced_input = encoded_df.drop(columns=cols_to_drop, errors='ignore')
    prediction = int(xg_clf.predict(reduced_input)[0])
    return {"prediction": prediction}

# -----------------------------------------------------------------------------------------------------------
                            # Run the FastAPI server (for testing locally)
# -----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
