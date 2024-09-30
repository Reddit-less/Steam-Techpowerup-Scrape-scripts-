from bs4 import BeautifulSoup
import requests
import json
import re

url = 'https://www.techpowerup.com/gpu-specs/geforce-rtx-3080.c3621'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

performance_entries = soup.find_all('div', class_='gpudb-relative-performance-entry')

data = []

for entry in performance_entries:
    gpu_link = entry.find('a', class_='gpudb-relative-performance-entry__link')
    if gpu_link:
        gpu_name = gpu_link.get_text().strip()
        performance_text = entry.find('div', class_='gpudb-relative-performance-entry__number').get_text().strip()
        performance_percentage = re.search(r'\d+', performance_text)
        if performance_percentage:
            gpu_entry = f"{gpu_name} ({performance_percentage.group(0)}%)"
            data.append(gpu_entry)
        else:
            gpu_entry = f"{gpu_name} (No valid percentage)"
            data.append(gpu_entry)
    else:
        print("Warning: A GPU entry without a valid name link was found and skipped.")

file_path = 'B:\\real data\\gpu_performance.json'

with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f'Data saved to {file_path}')
