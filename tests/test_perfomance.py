import time
from main import run_agents  # assuming run_agents triggers your workflow

def test_performance():
    start = time.time()
    run_agents()  # run your agent workflow
    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")
