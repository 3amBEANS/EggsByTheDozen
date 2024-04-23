import matplotlib.pyplot as plt
import numpy as np

# Step 1: Setup the plot
fig, ax = plt.subplots()

# Step 2: Add constant lines
# Constants
constants = [3, 24, 21]
labels = ['Parasite Count (Easy)', 'Parasite Count (Medium)', 'Parasite Count (Hard)']
colors = ['red', 'green', 'blue']

for constant, label, color in zip(constants, labels, colors):
    ax.axhline(y=constant, color=color, linestyle='-', label=f'{label} (Expected)')

# Step 3: Add empirical line graphs
# Initial data points for empirical values
#x_values = np.array([0, 1, 2, 3, 4, 5])  # Example x-values (e.g., time points)
#empirical_data = {
#    'Parasite number 1': constants[0] + np.random.normal(0, 1, len(x_values)),
#    'Parasite number 2': constants[1] + np.random.normal(0, 4, len(x_values)),
#    'Parasite number 3': constants[2] + np.random.normal(0, 2, len(x_values))
#}#

#for label, data in empirical_data.items():
#    ax.plot(x_values, data, label=f'{label} (empirical)', marker='o')

# Step 4: Customize the plot
ax.set_xlabel('Time')
ax.set_ylabel('Parasite Count')
ax.set_title('Parasite Observation Over Time')
ax.legend()

# Show the plot
plt.show()