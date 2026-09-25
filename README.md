# AI-RecoverX

AI-RecoverX is a controlled educational simulation for AI-assisted digital data recovery. It generates damaged file fragments with known ground truth so later phases can scan, match, reconstruct, measure, classify, and explain recovery results.

This project is not a replacement for professional forensic recovery software.

## Current scope: Phase 1 and Phase 2

- FastAPI health endpoint at `/api/health`
- CORS enabled for the future React frontend
- Deterministic damage simulator
- Supported input types: PDF, JPG/JPEG, PNG, TXT, DOCX, and ZIP
- Fragment shuffling, deletion, and byte corruption
- SHA-256 original hashes
- `data/ground_truth.json` with expected fragment order and damage labels
- Demo data that works without MongoDB or OpenAI

## Project layout

```text
backend/
  app/
    main.py
    core/
    api/
    models/
    recovery/
    ai/
    services/
  requirements.txt
  .env.example
scripts/
  generate_damage.py
data/
  original/
  damaged/
  recovered/
  ground_truth.json
python.py                 # existing Streamlit MVP
requirements.txt          # root development dependencies
```

## Setup

From PowerShell at the project root:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the interpreter directly:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the Phase 1 API

```powershell
Set-Location backend
..\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Expected health response:

```json
{"status":"ok","mode":"demo","version":"2.0.0"}
```

Verify it in another terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
```

## Run the Phase 2 simulator

From the project root:

```powershell
.\venv\Scripts\python.exe scripts\generate_damage.py
```

Optional controls:

```powershell
.\venv\Scripts\python.exe scripts\generate_damage.py --fragment-size 32 --damage-percent 30 --seed 42
```

Expected output resembles:

```text
Generated damaged fragments for 1 file(s).
Ground truth: ...\data\ground_truth.json
sample.txt: 5 fragments, 0 missing, 1 corrupted
```

The simulator writes shuffled fragment binaries to `data/damaged/` and metadata to `data/ground_truth.json`. Repeat the command with the same seed to reproduce the same result.

## Existing Streamlit MVP

The original demo remains available:

```powershell
.\venv\Scripts\python.exe -m streamlit run python.py --server.port 8501
```

## Next phases

The next requested phase is fragment signature detection and scanning. Later phases will add feature extraction, explainable ML matching, reconstruction, integrity analysis, FastAPI workflow APIs, React dashboard views, and optional MongoDB/OpenAI integrations.
