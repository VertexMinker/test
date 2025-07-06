from typing import List
import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_sales(sales_history: List[int]) -> float:
    """Simple linear regression forecast for next period."""
    if len(sales_history) < 2:
        return float(sales_history[-1] if sales_history else 0)

    X = np.arange(len(sales_history)).reshape(-1, 1)
    y = np.array(sales_history)
    model = LinearRegression()
    model.fit(X, y)
    next_period = np.array([[len(sales_history)]])
    return float(model.predict(next_period)[0])
