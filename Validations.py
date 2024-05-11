from datetime import datetime

class TaskValidator:
    @staticmethod
    def validateTaskData(data):
        title = data.get("title")
        description = data.get("description")
        priority = data.get("priority")
        due_date = data.get("due_date")
        category = data.get("category")

        errors = []

        if not title:
            errors.append("Title is missing")
            
        if priority is not None and not isinstance(priority, (int, float)) and priority < 0:
            errors.append("Priority must be a number greater than or equal to 0")

        if due_date is not None:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    errors.append("Due date must be in the format YYYY-MM-DD")


        return not errors, errors
