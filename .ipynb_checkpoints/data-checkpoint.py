import pandas as pd
import numpy as np

# Define the parameters
education_levels = ["Bachelors", "Masters", "PhD"]
n_samples = 1000

# Generate random data
np.random.seed(42)
education_qualification = np.random.choice(education_levels, n_samples)
years_of_experience = np.random.randint(0, 21, n_samples)
base_salary = 300000
max_salary = 5000000

# Create a salary function based on education and experience
def generate_salary(edu, exp):
    if edu == "Bachelors":
        return base_salary + exp * 50000 + np.random.randint(0, 100000)
    elif edu == "Masters":
        return base_salary + exp * 70000 + np.random.randint(50000, 150000)
    elif edu == "PhD":
        return base_salary + exp * 90000 + np.random.randint(100000, 200000)

salary = [generate_salary(edu, exp) for edu, exp in zip(education_qualification, years_of_experience)]

# Create the DataFrame
data = pd.DataFrame({
    'education_qualification': education_qualification,
    'years_of_experience': years_of_experience,
    'salary': salary
})

# Save the dataset to a CSV file
data.to_csv('software_engineer_salaries_india.csv', index=False)

print(data.head())
