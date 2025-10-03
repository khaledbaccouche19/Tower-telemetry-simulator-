# Local Chronos AI Service (CPU)

## Setup (macOS)

```
cd /Users/mac/Desktop/PFE/Project/ai-service
python3 -m venv venv
source venv/bin/activate
pip install -U "chronos-forecasting[torch]" fastapi uvicorn pydantic numpy
```

## Run

```
uvicorn app:app --host 127.0.0.1 --port 8000
```

## Test

```
curl -s -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"series":[32.1,32.5,32.9,33.0,33.2,33.1,33.4,33.6,33.8,33.7], "horizon": 20}'
```

Integrate by POSTing recent metric windows from the backend to `/predict`. The response contains a forecast and a simple severity signal for building alerts.
