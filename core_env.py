import os
import shutil
import sqlite3
import pandas as pd
from typing import Tuple, Dict, Any
from models import Action, Observation, State, Reward
from tasks import TASKS, TaskGrader

class SQLiteRetailEnv:
    def __init__(self, task_idx: int = 0):
        self.task_idx = task_idx
        self.db_path = f"sandbox_{task_idx}.db"
        self.score = 0.0
        self.is_done = False
        
    def _create_sandbox_db(self):
        # Create a fresh database from init.sql
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
        conn = sqlite3.connect(self.db_path)
        with open("data/init.sql", 'r') as f:
            script = f.read()
        conn.executescript(script)
        conn.commit()
        conn.close()

    def reset(self) -> Tuple[Observation, Dict[str, Any]]:
        self.score = 0.0
        self.is_done = False
        self._create_sandbox_db()
        task = TASKS[self.task_idx]
        
        info = {
            "instruction": task["instruction"],
            "schema_hint": "Tables: users, categories, products, orders, order_items"
        }
        obs = Observation(result="Environment reset successfully. Database is ready.")
        return obs, info

    def step(self, action: Action) -> Tuple[Observation, float, bool, bool, Dict[str, Any]]:
        if self.is_done:
            return Observation(result=""), self.score, True, False, {"error": "Environment is already done."}
        
        # If agent is submitting an answer
        if action.submit_answer is not None:
            print(f"EVALUATING ANSWER: '{action.submit_answer}'")
            grader = TaskGrader(self.db_path)
            task = TASKS[self.task_idx]
            grader_func = getattr(grader, task["grader_method"])
            
            self.score = grader_func(action.submit_answer)
            self.is_done = True
            print(f"FINAL SCORE RETURNED BY GRADER: {self.score}")
            
            obs = Observation(result="Answer submitted.")
            info = {"final_score": self.score}
            reward_obj = Reward(value=self.score, reason="Task graded strictly by grader.")
            return obs, reward_obj, self.is_done, False, info
            
        # Execution phase
        error = None
        result_str = ""
        step_reward_val = 0.0
        reason = "Blank Query"
        
        try:
            if not action.query:
                raise ValueError("No query and no answer submitted.")
                
            conn = sqlite3.connect(self.db_path)
            q_upper = action.query.strip().upper()
            
            if q_upper.startswith(("SELECT", "PRAGMA")):
                df = pd.read_sql_query(action.query, conn)
                result_str = df.to_string()
                step_reward_val = 0.05
                reason = "Valid syntax. Table extracted."
            elif q_upper.startswith(("DROP", "DELETE")):
                step_reward_val = -0.5
                reason = "Warning: Destructive actions penalize trajectory score."
                cursor = conn.cursor()
                cursor.execute(action.query)
                conn.commit()
                result_str = "Rows deleted/dropped."
            else:
                cursor = conn.cursor()
                cursor.execute(action.query)
                conn.commit()
                result_str = f"Query executed successfully. Rows affected: {cursor.rowcount}"
                step_reward_val = 0.1
                reason = "Mutation query executed."
                
            conn.close()
            
        except Exception as e:
            error = str(e)
            result_str = "Error executing query."
            step_reward_val = -0.1
            reason = f"Syntax or execution Error: {str(e)[:50]}"
            
        obs = Observation(result=result_str, error=error)
        reward_obj = Reward(value=step_reward_val, reason=reason)
        
        return obs, reward_obj, self.is_done, False, {}
        
    def state(self) -> State:
        task = TASKS[self.task_idx]
        return State(
            current_task=self.task_idx,
            task_level=task["level"],
            score=self.score,
            is_done=self.is_done
        )
