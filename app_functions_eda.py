# All imports
import uuid

import matplotlib.pyplot as plt
import pandas as pd


def task_1(df_full):
    try:
        return_string = ""
        image_saved = False

        # Select the specific column
        df_selected = df_full[['Wind Speed (m/s)']]

        # Set the data type for the selected column
        df_selected = df_selected.astype({'Wind Speed (m/s)': 'float64'})

        # Analyze distribution of Wind Speed values
        plt.figure(figsize=(10, 6))
        plt.hist(df_selected['Wind Speed (m/s)'], bins=30, color='skyblue', edgecolor='black')
        plt.title('Distribution of Wind Speed (m/s)')
        plt.xlabel('Wind Speed (m/s)')
        plt.ylabel('Frequency')
        plt.xticks(rotation=90)
        plt.grid(axis='y', alpha=0.75)
        plt.autoscale(enable=True, axis='both', tight=True)

        # Generate a unique UUID
        unique_id = uuid.uuid4()

        # Save the figure with a unique UUID in the file name
        plt.savefig(f"images/task_1/wind_speed_distribution_{unique_id}.png", bbox_inches='tight')
        plt.clf()

        image_saved = True
        return return_string, image_saved

    except Exception as e:
        print(f"Error occurred during execution of task_1: {e}")
        return None, None






def task_2(df_full):
    try:
        return_string = ""
        image_saved = False

        # Load the data

        # Step 2: Select the specific column after reading the data
        df = df_full[['Wind Direction (°)']]

        # Ensure the 'Wind Direction (°)' column is of type float64
        df['Wind Direction (°)'] = df['Wind Direction (°)'].astype('float64')

        # Plotting the Wind Direction data to study patterns
        plt.figure(figsize=(12, 6))
        plt.hist(df['Wind Direction (°)'], bins=36, edgecolor='black')
        plt.title('Distribution of Wind Direction (°)')
        plt.xlabel('Wind Direction (°)')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.xticks(rotation=90)
        plt.autoscale(enable=True, axis='both', tight=True)

        # Generate a unique UUID
        unique_id = uuid.uuid4()

        # Save the plot with a unique UUID in the file name
        plt.savefig(f"images/task_2/wind_direction_distribution_{unique_id}.png", bbox_inches='tight')

        # Clear the figure after saving
        plt.clf()

        image_saved = True
        return return_string, image_saved

    except Exception as e:
        print(f"Error occurred during execution of task_2: {e}")
        return None, None




def task_3(df_full):
    try:
        return_string = ""
        image_saved = False

        # Step 1: Select specific columns from the DataFrame
        df = df_full[['Date/Time', 'LV ActivePower (kW)']]

        # Ensure the correct datatype for 'Date/Time'
        df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

        # Ensure the correct datatype for 'LV ActivePower (kW)'
        df['LV ActivePower (kW)'] = df['LV ActivePower (kW)'].astype('float64')

        # Placeholder for negative readings logic
        negative_readings = df[df['LV ActivePower (kW)'] < 0].shape[0]
        interim_result = f"Negative power readings: {negative_readings}"
        return_string = return_string + str(interim_result) + '\n'

        # Placeholder for inconsistent readings logic
        inconsistent_readings = df['LV ActivePower (kW)'].isna().sum()
        print(f"Inconsistent readings (missing/NaN): {inconsistent_readings}")

        return return_string, image_saved

    except Exception as e:
        print(f"Error occurred during execution of task_3: {e}")
        return None, None

