# Preview isi predictor.py — kamu akan buat file ini manual di assessment/ml/

predictor_code = '''
import joblib
import numpy as np
import json
from pathlib import Path

# Load model dan metadata sekali saat module di-import
_dir = Path(__file__).parent
_model = joblib.load(_dir / 'model.joblib')

with open(_dir / 'model_metadata.json') as f:
    _metadata = json.load(f)

FEATURE_NAMES = _metadata['feature_names']
THRESHOLDS = _metadata['risk_thresholds']
NEEDS_SCALING = _metadata['needs_scaling']

if NEEDS_SCALING:
    _scaler = joblib.load(_dir / 'scaler.joblib')


def predict_risk(form_data: dict) -> dict:
    """
    Terima dict dari form Django, return risk prediction.
    
    Args:
        form_data: dict dengan key = nama kolom BRFSS
                   contoh: {'HighBP': 1, 'HighChol': 0, 'BMI': 28, ...}
    
    Returns:
        dict: {'probability': 45.2, 'tier': 'Moderate', 'feature_importance': {...}}
    """
    # Susun fitur dalam urutan yang BENAR
    features = np.array([[form_data[feat] for feat in FEATURE_NAMES]])
    
    # Scaling kalau perlu
    if NEEDS_SCALING:
        features = _scaler.transform(features)
    
    # Prediksi probabilitas
    proba = _model.predict_proba(features)[0][1]
    
    # Tentukan risk tier
    if proba < THRESHOLDS['low_max']:
        tier = 'Low'
    elif proba < THRESHOLDS['moderate_max']:
        tier = 'Moderate'
    else:
        tier = 'High'
    
    return {
        'probability': round(float(proba) * 100, 1),
        'tier': tier,
    }
'''

print(predictor_code)