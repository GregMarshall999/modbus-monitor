# Using a virtual environment (venv)

## 1. Create the virtual environment

From the project folder:

```powershell
python -m venv .venv
```

## 2. Activate the virtual environment

**Linux:**

```bash
source .venv/bin/activate
```

**PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Command Prompt (cmd):**

```cmd
.venv\Scripts\activate.bat
```

## 3. Install dependencies and run the app

With the venv activated (`(.venv)` in the prompt):

```powershell
pip install -r requirements.txt
uvicorn main:app --reload
```

http://127.0.0.1:8000 in browser.

## 4. Install test dependencies and run tests

With the venv activated, install dev dependencies (includes pytest and project deps):

```powershell
pip install -r requirements-dev.txt
```

Run the test suite (no USB device required; Modbus is mocked):

```powershell
pytest
```

Verbose output with coverage:

```powershell
pytest -v --cov=main --cov-report=term-missing
```

## 5. Deactivate when finished

```powershell
deactivate
```

---

## Quick reference

| Step | Command |
|------|---------|
| Create venv | `python -m venv .venv` |
| Activate (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Activate (cmd) | `.venv\Scripts\activate.bat` |
| Install dependencies | `pip install -r requirements.txt` |
| Install deps + test tools | `pip install -r requirements-dev.txt` |
| Run API | `uvicorn main:app --reload` |
| Run tests | `pytest` |
| Deactivate | `deactivate` |