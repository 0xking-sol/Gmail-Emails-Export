import imaplib
import email
import pandas as pd
from email.header import decode_header

# Your Gmail email and password
email_address = "Your_email_address_here"


email_password = "Your_accounts_password_here"

# Connect to the Gmail server using IMAP
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(email_address, email_password)

# Select the "inbox" mailbox
mail.select("inbox")

# Queries can have the following structure of "'Date' (Search Query)", in a list, or individually
search_queries = [
    'SINCE "01-MAR-2022" (OR SUBJECT "your application" BODY "your application")',
    'SINCE "01-MAR-2022" (OR SUBJECT "your CV" BODY "your CV")',
]

all_messages = []  # List to store all message IDs

# Fetch and process emails matching the search queries
for query in search_queries:
    _, msg_ids = mail.search(None, query)
    messages = msg_ids[0].decode().split()
    all_messages.extend(messages)  # Add the message IDs to the all_messages list


email_data = []
email_df = pd.DataFrame()

# Iterate through each email. I advise a try catch loop for most cases unless you need high precision 
for msg_id in all_messages:
    try:
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Check if Subject is not None before decoding
                if msg["Subject"]:
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)
                else:
                    subject = "Unknown Subject"

                from_ = msg["From"] if msg["From"] else "Unknown From"
                date_ = msg["Date"] if msg["Date"] else "Unknown Date"

                email_data.append({"Subject": subject, "From": from_, "Date": date_})
                print(date_)

    except Exception as e:
        print("Exception caught:", e)

# Create a DataFrame from the email data
email_df = pd.DataFrame(email_data)

# Save to CSV
email_df.to_csv("file_name", index=False)


