import subprocess
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter


# Define the terminal command
command = "cat /var/log/syslog"

# Run the command and capture the output
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Print the output
# print(result.stdout)
f = open("logs.log", "w")
f.write(result.stdout)
f.close()

num_lines = len(result.stdout.splitlines())
print("Number of lines:", num_lines)

log_counts = {}

# Open the log file and read line by line
with open("logs.log", "r") as file:
    # Extract event types from each line
    event_types = [line.split()[5] for line in file]

# Count the occurrences of each event type
event_counts = Counter(event_types)

# Calculate total count of all events
total_events = sum(event_counts.values())

# Create a list to store keys that need to be removed
keys_to_remove = []

# Iterate over event counts to identify events with less than 1% occurrence
for event, count in event_counts.items():
    percentage = (count / total_events) * 100
    if percentage < 2:
        keys_to_remove.append(event)

# Remove keys from event_counts dictionary
for key in keys_to_remove:
    event_counts.pop(key)

# Label all miscellaneous events as "Miscellaneous"
event_counts['Misc.'] = sum(count for event, count in event_counts.items())


# Bar chart
plt.figure(figsize=(10, 6))
plt.bar(event_counts.keys(), event_counts.values(), color='skyblue')
plt.xlabel('Event Types')
plt.ylabel('Frequency')
plt.title('Event Frequency')

# Display bar chart without blocking
plt.show(block=False)

# Pie chart
plt.figure(figsize=(10, 6))
plt.pie(event_counts.values(), labels=event_counts.keys(), autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Event Distribution')

# Display pie chart without blocking
plt.show(block=False)

# Print event counts for evaluation
print("Event Counts:")
for event, count in event_counts.items():
    print(f"{event}: {count}")

# Keep plots open
plt.show()