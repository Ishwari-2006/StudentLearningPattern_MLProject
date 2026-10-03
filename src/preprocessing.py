import pandas as pd


def load_data(file_path):
    """Load the student dataset."""
    return pd.read_csv(file_path)


def create_transactions(df):
    """
    Convert each student record into a transaction
    containing the items that apply to that student.
    """

    transactions = []

    for _, row in df.iterrows():
        transaction = []

        # Binary learning activities
        if str(row["Video_Lectures"]).lower() in ["yes", "1", "true"]:
            transaction.append("Video Lectures")

        if str(row["Notes"]).lower() in ["yes", "1", "true"]:
            transaction.append("Notes")

        if str(row["Practice_Problems"]).lower() in ["yes", "1", "true"]:
            transaction.append("Practice Problems")

        if str(row["Revision"]).lower() in ["yes", "1", "true"]:
            transaction.append("Revision")

        if str(row["Mock_Tests"]).lower() in ["yes", "1", "true"]:
            transaction.append("Mock Tests")

        if str(row["Group_Study"]).lower() in ["yes", "1", "true"]:
            transaction.append("Group Study")

        if str(row["Assignments_Completed"]).lower() in ["yes", "1", "true"]:
            transaction.append("Assignments Completed")

        # Categorical attributes
        if pd.notna(row["Study_Time"]):
            transaction.append(f"Study Time: {row['Study_Time']}")

        if pd.notna(row["Attendance"]):
            transaction.append(f"Attendance: {row['Attendance']}")

        if pd.notna(row["Primary_Resource"]):
            transaction.append(f"Resource: {row['Primary_Resource']}")

        # Performance
        if pd.notna(row["Performance"]):
            transaction.append(f"Performance: {row['Performance']}")

        transactions.append(set(transaction))

    return transactions


def prepare_transactions(file_path):
    """Load data and convert it into transactions."""
    df = load_data(file_path)
    transactions = create_transactions(df)

    return df, transactions