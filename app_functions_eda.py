# All imports
import uuid

import matplotlib.pyplot as plt
import pandas as pd


def task_1(df):
    try:
        return_string = ""
        image_saved = False

        # Load the data from the CSV file

        # Step 2: Select specific columns
        df = df[['LV ActivePower (kW)', 'Wind Speed (m/s)']]

        # Step 3: Set the data types for the selected columns
        df = df.astype({'LV ActivePower (kW)': 'float64', 'Wind Speed (m/s)': 'float64'})
        correlation = df['Wind Speed (m/s)'].corr(df['LV ActivePower (kW)'])
        interim_result = f"Correlation between Wind Speed (m/s) and LV ActivePower (kW): {correlation}"
        return_string = return_string + str(interim_result) + '\n'

        return return_string, image_saved

    except Exception as e:
        print(f"Error occurred during execution of task_1: {e}")
        return None, None






def task_8(df):
    try:
        return_string = ""
        image_saved = False

        # Select the specific columns you need
        df = df[['Wind Speed (m/s)', 'Wind Direction (°)']]

        # Set the data types for the selected columns
        df = df.astype({'Wind Speed (m/s)': 'float64', 'Wind Direction (°)': 'float64'})

        # Plotting Wind Speed vs Wind Direction
        plt.figure(figsize=(12, 8))  # Set a suitable figure size
        plt.scatter(df['Wind Direction (°)'], df['Wind Speed (m/s)'], alpha=0.5, label='Data Points')
        plt.title('Wind Speed vs Wind Direction')
        plt.xlabel('Wind Direction (°)')
        plt.ylabel('Wind Speed (m/s)')
        plt.grid(True)
        plt.xticks(rotation=90)  # Rotate x-axis labels
        plt.autoscale()  # Autoscale the limits of the axes
        plt.legend()

        # Generate a unique UUID
        unique_id = uuid.uuid4()

        # Save the plot with a unique UUID in the file name
        plt.savefig(f"images/task_8/wind_speed_vs_direction_{unique_id}.png", bbox_inches='tight')
        plt.clf()  # Clear the figure after saving

        image_saved = True
        return return_string, image_saved

    except Exception as e:
        print(f"Error occurred during execution of task_8: {e}")
        return None, None

