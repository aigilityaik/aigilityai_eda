import os
import inspect
import app_functions_eda
import json
import shutil
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

import warnings
warnings.filterwarnings("ignore")

IMAGE_SOURCE_FOLDER = "images"


def handle_missing_values(df):
    """
    Handles missing values in a pandas DataFrame by using appropriate imputation techniques
    for numerical and categorical columns.

    Parameters:
    df (pd.DataFrame): The input DataFrame with missing values.

    Returns:
    pd.DataFrame: A new DataFrame with missing values handled.
    """

    try:
        # if empty dataframe in parameter
        if df.empty:
            return df

        # Separate numerical and categorical columns
        numerical_cols, categorical_cols = [], []

        try:
            numerical_cols = df.select_dtypes(include=[np.number]).columns.to_list()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.to_list()
        except ValueError as e:
            numerical_cols, categorical_cols = [], []


        # Create imputers for numerical and categorical columns
        # For numerical columns, let's use the mean to fill in missing values
        numerical_imputer = SimpleImputer(strategy='mean')

        # For categorical columns, we'll use the most frequent value (mode)
        categorical_imputer = SimpleImputer(strategy='constant', fill_value='UNKNOWN', missing_values=None)

        # Impute the missing values
        if numerical_cols:
            df[numerical_cols] = numerical_imputer.fit_transform(df[numerical_cols])
        if categorical_cols:
            df[categorical_cols] = categorical_imputer.fit_transform(df[categorical_cols])

        return df

    except Exception as e:
        print(f"error while handling missing values: {e}")
        return df


def check_assertions_and_read_data(file_path, carryover_details_json):
    """Checks assertions related to file extension, if file is empty, and column names, 
    then reads data from the file into a DataFrame.

    Args:
        file_path (str): The path to the file.
        carryover_details_json (dict): JSON object containing details to validate against.

    Returns:
        pandas.DataFrame: DataFrame containing the data read from the file.

    Raises:
        AssertionError: If any of the assertions fail.
        Exception: If there is an error during file reading or assertion checks.
    """
    try:
        # Asserting file extension
        file_extension = file_path.split('.')[-1].lower()  # Get file extension

        # Reading data from the file based on its extension
        data_received_df = pd.DataFrame()
        if file_extension == "csv":
            data_received_df = pd.read_csv(file_path)
        elif file_extension in ["xlsx", "xls"]:
            data_received_df = pd.read_excel(file_path)

        # Checking if file is empty
        assert data_received_df.shape[0] > 0, "File is empty"

        # Asserting column names
        expected_column_names = carryover_details_json["column_names"]
        actual_column_names = list(set(data_received_df.columns))
        assert all(column in expected_column_names for column in actual_column_names), \
            "Column names do not match or some columns are missing."

        # handle missing values in the dataframe
        data_received_df = handle_missing_values(data_received_df.copy())

        return data_received_df

    except AssertionError as assertion_error:
        print(assertion_error)
        response = str(assertion_error)
        return response

    except Exception as e:
        print(e)
        response = str("Problem Occurred while reading file\n")
        return response
    

def run_all_functions_and_update_json(functions, data, tasks, task_names, tasks_feedbacks_json):
    """
    Run all functions, update JSON with results, and move images if saved.

    Args:
        functions (list): List of functions to execute.
        data (pd.DataFrame): Data to be passed to functions.
        tasks (list): List of tasks to update.
        task_names: The name of functions
        tasks_feedbacks_json: tasks dictionary with their single/concatenated feedbacks if any

    Returns:
        tuple: Updated tasks list and flag indicating successful execution.
    """
    try:
        # Execute all functions
        for i, ((name, func), task, task_name) in enumerate(zip(functions, tasks, task_names), start=1):

            if name != task_name:
                continue

            print(f"Executing {name}........... ")

            # create images folder if not exist and task folder inside images folder
            if not os.path.exists(IMAGE_SOURCE_FOLDER):
                os.makedirs(IMAGE_SOURCE_FOLDER)

            if not os.path.exists(f"{IMAGE_SOURCE_FOLDER}/{task_name}"):
                os.makedirs(f"{IMAGE_SOURCE_FOLDER}/{task_name}")

            try:
                result, image_saved = func(data.copy())

                image_list = []
                if image_saved:
                    # Define the source and destination folders
                    destination_folder = "static"  # Update with your destination folder path

                    # Create the destination folder if it doesn't exist and task folder inside destination folder
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)

                    if not os.path.exists(f"{destination_folder}/{task_name}"):
                        os.makedirs(f"{destination_folder}/{task_name}")

                    # Iterate through files in the source folder
                    for filename in os.listdir(f"{IMAGE_SOURCE_FOLDER}/{task_name}"):
                        # Check if the item is a file
                        if os.path.isfile(os.path.join(f"{IMAGE_SOURCE_FOLDER}/{task_name}/", filename)):
                            # Prepend '1' to the filename
                            new_filename = f"{i}_" + filename
                            # Construct the full paths for source and destination
                            source_path = os.path.join(f"{IMAGE_SOURCE_FOLDER}/{task_name}/", filename)
                            destination_path = os.path.join(destination_folder, f"{task_name}", new_filename)
                            destination_path = "./" + destination_path

                            image_list.append(destination_path)
                            shutil.move(source_path, destination_path)

                    print(f"Image(s) saved in: {destination_folder} folder")

                # Update task details
                task["stdout"] = result
                task["images_saved"] = image_list
                task["reject_feedback"] = tasks_feedbacks_json[task_name]

                print("---------Execution Completed---------\n")

                # Remove images folder
                if os.path.exists(IMAGE_SOURCE_FOLDER):
                    shutil.rmtree(IMAGE_SOURCE_FOLDER)

            except Exception as e:
                print(f"Error occurred during function execution during deployment: func_name = {name}:\n{e}")
                continue

        return tasks, True

    except Exception as e:
        print(f"Error occurred during function execution: {e}")
        return tasks, False


def process_app(file_path):
    """
    Process generated application
    """
    try:

        if file_path:

            # create tasks folder in images if does not exist
            with open("task_names.json", "r") as file:
                task_names = json.load(file)

            # Read carryover json containing carryover details such as extension, column names etc
            carryover_details_json_path = os.path.join("loader_output.json")
            with open(carryover_details_json_path, "r") as file_name:
                carryover_details_json = json.load(file_name)

            # Read task details json containing task details with their respective code
            tasks_details_json_path = os.path.join("coder_output.json")
            with open(tasks_details_json_path, "r") as file_name:
                tasks_details_json = json.load(file_name)

            # Read task feedback details json containing all tasks feedbacks
            tasks_feedbacks = os.path.join("tasks_feedbacks.json")
            with open(tasks_feedbacks, "r") as file_name:
                tasks_feedbacks_json = json.load(file_name)

            data_received_df = check_assertions_and_read_data(file_path, carryover_details_json)

            if not isinstance(data_received_df, pd.DataFrame):
                return f"{data_received_df.data.decode('utf-8')}\n"

            # Get all functions from app_functions module
            members = inspect.getmembers(app_functions_eda)
            funcs = [(name, member) for name, member in members if inspect.isfunction(member)]
            funcs.sort(key=lambda x: inspect.getsourcelines(x[1])[1])

            # Execute functions and update JSON
            task_json_with_op, execution_successful = run_all_functions_and_update_json(funcs, data_received_df, tasks_details_json, task_names["task_names"], tasks_feedbacks_json)

            with open("coder_output_updated.json", "w") as f:
                json.dump(task_json_with_op, f)

            returnable_json = {'EDA_output': task_json_with_op}

            return returnable_json
            
        else:
            print("Unable to read file")
        
    except Exception as e:
        print(f"Error occurred during upload: {e}")
        return "Execution failed\n"
