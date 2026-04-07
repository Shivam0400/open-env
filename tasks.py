import sqlite3

class TaskGrader:
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def grade_easy(self, agent_answer: str) -> float:
        # Easy Task: Calculate total revenue from COMPLETED orders.
        if agent_answer and "1609.95" in str(agent_answer):
            return 1.0
        return 0.0

    def grade_medium(self, agent_answer: str) -> float:
        # Medium Task: "Set the status of all orders placed by 'Diana Prince' to 'CANCELLED'."
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT status FROM orders o
                JOIN users u ON o.user_id = u.id
                WHERE u.name = 'Diana Prince'
            """)
            statuses = cursor.fetchall()
            conn.close()
            
            all_cancelled = all(s[0] == 'CANCELLED' for s in statuses)
            if len(statuses) > 0 and all_cancelled:
                return 1.0 # Success
            return 0.0
        except Exception:
            return 0.0

    def grade_hard(self, agent_answer: str) -> float:
        # Hard Task: "Return the name of the category that has the highest total revenue (from COMPLETED orders only). Just the name."
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.name, SUM(oi.quantity * oi.unit_price) as rev
                FROM categories c
                JOIN products p ON c.id = p.category_id
                JOIN order_items oi ON p.id = oi.product_id
                JOIN orders o ON oi.order_id = o.id
                WHERE o.status = 'COMPLETED'
                GROUP BY c.id
                ORDER BY rev DESC
                LIMIT 1
            """)
            correct_category = str(cursor.fetchone()[0]).strip().lower()
            conn.close()
            
            if agent_answer and correct_category in str(agent_answer).lower().strip():
                return 1.0
            return 0.0
        except Exception:
            return 0.0

# Task definitions used by Env
TASKS = [
    {
        "level": "easy",
        "instruction": "Calculate the total revenue from all COMPLETED orders. Submit your answer as a single number using the submit_answer action parameter.",
        "grader_method": "grade_easy"
    },
    {
        "level": "medium",
        "instruction": "Update the database. Set the status of all orders placed by 'Diana Prince' to 'CANCELLED'. When done, submit any non-empty answer using submit_answer.",
        "grader_method": "grade_medium"
    },
    {
        "level": "hard",
        "instruction": "Calculate the name of the category that has the highest total revenue (from COMPLETED orders only). Submit the exact category name using the submit_answer action.",
        "grader_method": "grade_hard"
    }
]
