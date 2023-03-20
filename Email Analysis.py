import pandas as pd

# load the dataframe with job application emails
df = pd.read_csv('job_application_emails.csv')

# filter and clean the data
df = df[df['Subject'].str.contains('application|received|applying|next steps|recruitment team', case=False)]
df = df[~df['Subject'].str.contains('github', case=False)]
df = df.reset_index(drop=True)

# convert the date column to a datetime object and sort the dataframe
df['Date'] = pd.to_datetime(df['Date'], utc=True)
df = df.sort_values('Date')

# convert the date column to a human-readable format
df['Date'] = df['Date'].dt.strftime('%d %B %Y')

# save the filtered dataframe with human-readable dates to a csv file
df.to_csv('Filtered Emails.csv', index=False)

# randomly select a sample of 30 rows
sample_size = 30
sample = df.sample(n=sample_size, random_state=42)

# manually review the sample to determine the proportion of job application emails
sample.to_csv('30 Random Emails')

# use the proportion in the sample to estimate the total number of job application emails in the entire dataset
proportion = 24 / sample_size  # for example
total_emails = len(df)
estimated_job_application_emails = proportion * total_emails

print("Estimated number of job application emails: ", estimated_job_application_emails)
