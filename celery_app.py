from celery_app import add
import time

# Submit the task
result = add.delay(4, 6)
task_id = result.id
print(f"Task submitted, result will be available later. Task ID: {task_id}")

# Wait for the task to complete and get the result
try:
    while not result.ready():
        print("Waiting for task to complete...")
        time.sleep(1)  # Sleep for a second before checking again

    # Get the result
    if result.successful():
        print(f"Task result: {result.get(timeout=30)}")  # Adjust timeout if needed
    else:
        print("Task failed.")
except Exception as e:
    print(f"An error occurred: {e}")

