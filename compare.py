import json
import csv

CSV_FILENAME = 'metric_comparison.csv'

def parse_dataset(dataset):
    dataset_id = dataset["dataset-id"][0]["value"]
    metrics = {}

    # Extract and populate metric types and their values
    for metric_info in dataset["performance"][0]["instance"]:
        access_method = metric_info.get("access-method")

        # Only concerned with regular access methods
        if access_method == "regular":
            metric_type = metric_info["metric-type"]
            metric_value = metric_info["count"]
            metrics[metric_type] = metric_value

    return (dataset_id, metrics)

def add_to_comparison_data_map(identifier, comparison_data, datasets):
    for dataset in datasets:
        doi, metrics = parse_dataset(dataset)
        if doi not in comparison_data:
            comparison_data[doi] = {identifier: metrics}
        else:
            comparison_data[doi][identifier] = metrics

def write_csv_report(comparison_data, identifier_a='a', identifier_b='b'):
    filename = 'data/' + CSV_FILENAME
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write CSV header
        header = ["DOI", "Metric Type", "A Value", "B Value", "Difference", "Same?"]
        csv_writer.writerow(header)

        def get_value(metrics, metric_type):
            if identifier_a not in metrics:
                a_value = 0
            else:
                a_value = metrics[identifier_a].get(metric_type, 0)

            if identifier_b not in metrics:
                b_value = 0
            else:
                b_value = metrics[identifier_b].get(metric_type, 0)

            return (a_value, b_value)

        def get_metrics(metrics, metric_type):
            a_value, b_value = get_value(metrics, metric_type)

            difference = a_value - b_value

            if difference == 0:
                same = True
            else:
                same = False

            return (a_value, b_value, difference, same)


        # Write comparison data
        for dataset_id, metrics in comparison_data.items():
            metric_type = 'total-dataset-investigations'
            a_value, b_value, difference, same = get_metrics(metrics, metric_type)
            if a_value == 0 and b_value == 0:
                continue
            csv_writer.writerow([dataset_id, metric_type, a_value, b_value, difference, same])

            metric_type = 'unique-dataset-investigations'
            a_value, b_value, difference, same = get_metrics(metrics, metric_type)
            if a_value == 0 and b_value == 0:
                continue
            csv_writer.writerow([dataset_id, metric_type, a_value, b_value, difference, same])

            metric_type = 'total-dataset-requests'
            a_value, b_value, difference, same = get_metrics(metrics, metric_type)
            if a_value == 0 and b_value == 0:
                continue
            csv_writer.writerow([dataset_id, metric_type, a_value, b_value, difference, same])

            metric_type = 'unique-dataset-requests'
            a_value, b_value, difference, same = get_metrics(metrics, metric_type)
            if a_value == 0 and b_value == 0:
                continue
            csv_writer.writerow([dataset_id, metric_type, a_value, b_value, difference, same])

            # for metric_type in metrics[identifier_a]:
            #     if identifier_a not in metrics:
            #         a_value = 0
            #     else:
            #         a_value = metrics[identifier_a].get(metric_type, 0)

            #     if identifier_b not in metrics:
            #         b_value = 0
            #     else:
            #         b_value = metrics[identifier_b].get(metric_type, 0)

            #     difference = a_value - b_value
            #     if difference == 0:
            #         same = True
            #     else:
            #         same = False


def read_report_datasets(report_file):
    report_json = ''
    datasets = []

    # Read report json file
    with open(report_file, 'r') as report_file:
        report_json = json.loads(report_file.read())

    datasets = report_json['report-datasets']

    return datasets

def generate_comparison(report_a, report_b):

    datasets_a = read_report_datasets('data/' + report_a)
    datasets_b = read_report_datasets('data/' + report_b)

    comparison_data = {}

    add_to_comparison_data_map('a', comparison_data, datasets_a)
    add_to_comparison_data_map('b', comparison_data, datasets_b)

    write_csv_report(comparison_data)

    # for dataset_id, metrics in comparison_data.items():
    #     if "a" in metrics and "b" in metrics:
    #         print("Dataset ID:", dataset_id)
    #         for metric_type in metrics["a"]:
    #             a_value = metrics["a"][metric_type]
    #             b_value = metrics["b"].get(metric_type, 0)  # Use 0 if metric not in file2
    #             print(f"  Metric: {metric_type}")
    #             print(f"    A Value: {a_value}")
    #             print(f"    B Value: {b_value}")
    #             print(f"    Difference: {a_value - b_value}")

if __name__ == '__main__':
    generate_comparison('7898f875-dabe-4ec8-a857-7f81fd30c242.json', 'da-80l49bsf-2023-07-01-2023-07-31-1.json')