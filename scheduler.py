from apscheduler.schedulers.blocking import BlockingScheduler # type: ignore
import subprocess
import os

# Function to run login.py
def run_login():
    subprocess.run(["python", "login.py"], check=True)

# Function to run main.py
def run_main():
    subprocess.run(["python", "main.py"], check=True)

# Create a scheduler instance
scheduler = BlockingScheduler()

# Schedule login.py to run once every 2 days
scheduler.add_job(run_login, 'interval', days=2)

# Schedule main.py to run every day at 12 PM
scheduler.add_job(run_main, 'cron', hour=12, minute=0)

# Start the scheduler
try:
    print("Scheduler started. Press Ctrl+C to exit.")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("Scheduler shutting down...")
    scheduler.shutdown()
