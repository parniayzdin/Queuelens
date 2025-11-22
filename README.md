# Queuelens
QueueLens is a crowd-sourced web app that lets users report and view real-time queue wait times on an interactive map. Reports automatically age out after an hour and are weighted by freshness, so you always see the most relevant wait estimates.

# Features
- Search your destination!
- Report live wait times!
- Reports auto-expire!

# Overview
<img width="1553" height="782" alt="Screenshot 2025-07-21 192425" src="https://github.com/user-attachments/assets/d80f43c5-bf92-467c-97c4-b58eef14ce5c" />

# Quick Start
<details>
<summary>setup</summary>

## Backend
> Make sure this is done on Command Prompt Terminal.
> 
> Make sure you’re in the **project root** (`queuelens/`).
```bash
git clone https://github.com/parniayzdin/QueueLens.git

cd backend

# Install venv
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

uvicorn main:app --reload
```
## Frontend
```bash
cd frontend
npm install
npm run dev
```
</details>

# Example Usage
1. Search for a location (e.g. "Toronto")
2. View markers showing current reported wait times
3. Enter a wait time and submit to help others
4. Reports fade out after 1 hour to keep the data fresh
<div align="center"> Made by Parnia Yazdinia </div>





