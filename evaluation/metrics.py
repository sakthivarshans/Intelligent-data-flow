# This file helps calculate standard error scores.
from sklearn.metrics import precision_score, recall_score, f1_score, mean_absolute_error, mean_squared_error
import numpy as np

def calculate_classification_metrics(y_true, y_pred, labels=None):
    """
    Calculate Precision, Recall, F1 for classification tasks.
    """
    return {
        'precision': precision_score(y_true, y_pred, average='weighted', labels=labels, zero_division=0),
        'recall': recall_score(y_true, y_pred, average='weighted', labels=labels, zero_division=0),
        'f1': f1_score(y_true, y_pred, average='weighted', labels=labels, zero_division=0)
    }

def calculate_regression_metrics(y_true, y_pred):
    """
    Calculate MAE and RMSE for regression tasks.
    """
    mse = mean_squared_error(y_true, y_pred)
    return {
        'mae': mean_absolute_error(y_true, y_pred),
        'rmse': np.sqrt(mse)
    }

