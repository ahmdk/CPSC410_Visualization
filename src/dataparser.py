import csv
from pathlib import Path


root_path = Path(__file__).parent


def export_hit_count(src):
    f = open(Path(root_path/'data') / "hit_count.csv", "w")
    wr = csv.writer(f)
    for key, value in src.items():
        wr.writerow([key, value])
    f.close()


def export_run_time(src):
    f = open(Path(root_path/'data') / "run_time.csv", "w")
    wr = csv.writer(f)
    for key, value in src.items():
        for val in value:
            wr.writerow([key, val])
    f.close()


def create_output_directory():
    Path(root_path/'data').mkdir(parents=True, exist_ok=True)


hitCounts = {
  "method1": 2,
  "method2": 4,
  "method3": 3
}

# We can decide on the units for times, but seems like
# it's defined to seconds
runTimes = {
  "method1": [2, 3],
  "method2": [5, 4, 5, 6],
  "method3": [1, 1, 2, 1]
}

create_output_directory()
export_hit_count(hitCounts)
export_run_time(runTimes)
