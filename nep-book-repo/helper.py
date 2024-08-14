import random
import csv


def get_user_agent():
    with open("user-agents.txt") as f:
        agents = f.read().splitlines()
        return random.choice(agents)


def get_field_names_from_dict(a_dict):
    return a_dict.keys()


def write_to_file(title_and_links_list, file_name):
    csv_file = f"{file_name}.csv"
    fieldnames = get_field_names_from_dict(title_and_links_list[0])

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the rows
        for row in title_and_links_list:
            writer.writerow(row)


def read_links_from_csv(file_path):
    links = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            links.append(row[1])  # Append the link (second column)
    return links



