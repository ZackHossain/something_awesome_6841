def result(db_id, task_id, success, msg):
    return {
        "id": db_id,
        "result_id": task_id,
        "success": success,
        "content": msg
    }