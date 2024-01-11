import re # regex module
import mailbox # reading the mail file
from email.header import decode_header # decode header func
import email.utils # to parse the date and time
import csv
from datetime import datetime
import os

def PayTrackr(mboxfile):    
    pattern = r'\bSent\b \u20B9 \d+' # regex patter found in PhonePe emails
    amtpattern = r'\d+' #amount of money pattern
    spent = 0
    results = []

    mbox_file = mailbox.mbox(mboxfile)

    for message in mbox_file:
        subject = message['subject'] # store the email subject
        date = email.utils.parsedate_to_datetime(message['date']) # store the email date and time
        friendly_date = date.strftime("%A, %d %B %Y, %I:%M %p") # format the date and time
        day = date.strftime("%A") # store the day of the week
        date_only = date.strftime("%d %B %Y") # store the date only
        time = date.strftime("%I:%M %p") # store the time only
        decoded_value, charset = decode_header(subject)[0] # store the encoded subject and the charset used to encode it

        # decode the subject
        if isinstance(decoded_value, bytes):
            if charset is None:
                charset = 'utf-8'
            decoded_value = decoded_value.decode(charset)

        match = re.search(pattern, decoded_value)
        if match:
            match = re.search(amtpattern, decoded_value)
            spent += int(match.group())
            results.append({"day":day, "date":date_only, "time":time, "subject":decoded_value, "amount":match.group()})

        # Define the CSV filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        os.makedirs('transaction_files', exist_ok=True) # create the directory if it doesn't exist
        csv_filename = os.path.join('transaction_files', f"transactions_{timestamp}.csv")
        
        # Write the results to a csv file
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Day', 'Date', 'Time', 'Subject', 'Amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow({
                    'Day': result['day'],
                    'Date': result['date'],
                    'Time': result['time'],
                    'Subject': result['subject'],
                    'Amount': result['amount']
                })
    # Return the results and the total amount spent and the csv filename
    return results, spent, csv_filename

   
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mbox'
