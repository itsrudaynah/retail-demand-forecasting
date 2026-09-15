import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


FORECAST_HORIZON = 15


EXCLUDED_EVALUATION_SERIES = [
    (6, "BABY CARE")
]


def filter_evaluation_data(df):
    """
    Removes Store × Family series that have no eligible training rows
    after feature engineering, so they cannot be evaluated fairly
    against models trained on the prepared training dataset.
    """

    return df[
        ~df[["store_nbr", "family"]]
        .apply(tuple, axis=1)
        .isin(EXCLUDED_EVALUATION_SERIES)
    ].copy()


def evaluate(actual, prediction, name="Model"):
    """
    Computes MAE, RMSE, RMSLE, and WMAPE.

    RMSLE is the primary evaluation metric.
    MAE, RMSE, and WMAPE are supporting metrics.
    """

    actual = np.array(actual)

    prediction = np.clip(
        np.array(prediction),
        0,
        None
    )

    mae = mean_absolute_error(
        actual,
        prediction
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            prediction
        )
    )

    rmsle = np.sqrt(
        np.mean(
            (
                np.log1p(prediction)
                - np.log1p(actual)
            ) ** 2
        )
    )

    total_actual = np.sum(
        np.abs(actual)
    )

    if total_actual == 0:
        wmape = np.nan

    else:
        wmape = (
            np.sum(
                np.abs(actual - prediction)
            )
            /
            total_actual
            * 100
        )

    print(
        f"{name:20s} "
        f"MAE: {mae:8.2f} | "
        f"RMSE: {rmse:8.2f} | "
        f"RMSLE: {rmsle:.4f} | "
        f"WMAPE: {wmape:6.2f}%"
    )

    return {
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "RMSLE": rmsle,
        "WMAPE": wmape
    }