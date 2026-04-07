from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core_env import SQLiteRetailEnv
from models import Action, Observation, State, Reward

app = FastAPI(title="OpenEnv - SQLite Retail Data")

# Global dict to hold environment instances per session
envs = {}

class ResetRequest(BaseModel):
    session_id: str
    task_idx: int = 0

class StepRequest(BaseModel):
    session_id: str
    action: Action

@app.post("/reset")
def reset(req: ResetRequest):
    env = SQLiteRetailEnv(task_idx=req.task_idx)
    envs[req.session_id] = env
    obs, info = env.reset()
    return {"observation": obs, "info": info}

@app.post("/step")
def step(req: StepRequest):
    if req.session_id not in envs:
        raise HTTPException(status_code=400, detail="Session not found, call /reset first.")
    
    print(f"DEBUG: Receiving action for session {req.session_id}: {req.action}")
    env = envs[req.session_id]
    obs, reward, done, truncated, info = env.step(req.action)
    
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "truncated": truncated,
        "info": info
    }

@app.post("/state")
def state(req: ResetRequest):  # Can reuse ResetRequest just for session_id
    if req.session_id not in envs:
        raise HTTPException(status_code=400, detail="Session not found.")
    
    env = envs[req.session_id]
    return env.state()

if __name__ == "__main__":
    import uvicorn
    # 7860 is the standard port for Hugging Face Spaces (Docker spaces)
    uvicorn.run(app, host="0.0.0.0", port=7860)
