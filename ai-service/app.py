from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import torch

try:
    # Chronos is optional at creation time; user installs per README
    from chronos import ChronosPipeline
except Exception as e:  # pragma: no cover
    ChronosPipeline = None  # type: ignore


class PredictIn(BaseModel):
    series: List[float]
    horizon: int = 30
    quantiles: Optional[List[float]] = [0.1, 0.5, 0.9]


class PredictOut(BaseModel):
    forecast: List[float]
    q10: Optional[List[float]] = None
    q90: Optional[List[float]] = None
    residuals: Optional[List[float]] = None
    severity: str


app = FastAPI(title="Local Chronos AI Service", version="0.1.0")


def _load_pipe():
    if ChronosPipeline is None:
        raise RuntimeError(
            "chronos package not installed. Run: pip install -U 'chronos-forecasting[torch]'"
        )
    return ChronosPipeline.from_pretrained(
        "amazon/chronos-t5-small",
        device_map="cpu",
        torch_dtype=torch.float32,
    )


pipe = None


@app.on_event("startup")
def _startup():  # pragma: no cover
    global pipe
    pipe = _load_pipe()


@app.post("/predict", response_model=PredictOut)
def predict(req: PredictIn):
    if pipe is None:  # pragma: no cover
        raise RuntimeError("Model not loaded")

    arr = np.asarray(req.series, dtype=np.float32)
    if arr.size == 0:
        return PredictOut(forecast=[], q10=None, q90=None, residuals=None, severity="INFO")

    # fill tiny gaps and normalize
    mean = float(np.nanmean(arr)) if np.isfinite(np.nanmean(arr)) else 0.0
    arr = np.nan_to_num(arr, nan=mean)
    std = float(arr.std() or 1.0)
    norm = (arr - mean) / std

    # Chronos expects a list[Tensor]
    contexts = [torch.tensor(norm.tolist(), dtype=torch.float32)]
    pred = pipe.predict(contexts, req.horizon)

    # Unpack first series and convert to numpy
    if isinstance(pred, (list, tuple)):
        first = pred[0]
    else:
        first = pred
    if hasattr(first, "tolist"):
        seq = first.tolist()
    else:
        seq = list(first)

    arr_pred = np.asarray(seq, dtype=np.float32)
    # If multi-sample (2D), average across last axis to get a single path
    if arr_pred.ndim >= 2:
        arr_pred = arr_pred.reshape(arr_pred.shape[0], -1).mean(axis=-1)

    f = arr_pred * std + mean

    band = float(abs(f - mean).mean())
    severity = "CRITICAL" if band > std * 1.5 else ("HIGH" if band > std else "INFO")

    return PredictOut(
        forecast=f.astype(float).tolist(),
        q10=None,
        q90=None,
        residuals=None,
        severity=severity,
    )


