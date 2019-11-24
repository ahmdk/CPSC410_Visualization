import csv
import argparse
import json
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("data", help="path to the analyzed data file")
args = parser.parse_args()
directory = args.data

root_path = Path(__file__).parent


def export_run_time():
    f = open(Path(root_path/'data') / "run_time.csv", "w")
    wr = csv.writer(f)

    wr.writerow(["file_name", "method", "runtime"])

    output_json = json.load(open(directory))

    for major_key, value in output_json.items():
        split_string = major_key.split(';')
        file_name = split_string[0]
        func_name = split_string[1]

        for val in value:
            wr.writerow([file_name, func_name, float(val["duration"])*1000.0])  # to ms

    f.close()


def create_output_directory():
    Path(root_path/'data').mkdir(parents=True, exist_ok=True)


create_output_directory()
export_run_time()
