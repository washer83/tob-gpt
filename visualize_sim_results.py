import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import seaborn as sns

def plot_kill_time_distributions_and_stats(file_paths, labels=None):
    """
    Plot kill time distributions from multiple CSV files and display statistics.
    
    :param file_paths: List of file paths to the CSV files
    :param labels: List of labels for the plots (Optional). Defaults to filenames.
    """
    plt.figure(figsize=(10, 6))
    stats_data = []
    
    for i, file_path in enumerate(file_paths):
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Use provided label or default to filename
        label = labels[i] if labels and i < len(labels) else file_path.split('/')[-1]
        
        # Plot the histogram for 'ticks_until_defeat' with transparency
        plt.hist(df['ticks_until_defeat'], bins=30, alpha=0.5, label=label)
        
        # Add a smoothed line (KDE)
        #sns.kdeplot(df['ticks_until_defeat'], label=f"{label} Smoothed")
        
        # Calculate statistics
        mean_value = df['ticks_until_defeat'].mean()
        median_value = df['ticks_until_defeat'].median()
        
        # Store the stats
        stats_data.append([label, f"Mean: {mean_value:.2f}", f"Median: {median_value:.2f}"])

    plt.title('Red Proc Distributions')
    plt.xlabel('Ticks Until Reds')
    plt.ylabel('Density')
    plt.legend()
    plt.show()
    
    # Display the statistics in a table format
    print(tabulate(stats_data, headers=['Dataset', 'Mean', 'Median'], tablefmt='grid'))

# Example usage:
file_paths = ['8_way_mage_no_boots_results.csv', '6_way_mage_no_boots_results.csv', 'duo_rancor_results.csv', 'duo_bf_results.csv']
labels = ['8 way mage', '6 way mage', 'Rancor', 'Blood fury']
plot_kill_time_distributions_and_stats(file_paths, labels)
