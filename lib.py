from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from collections import defaultdict
import math
import csv
import sys
import requests
import uuid
import os
import pandas as pd
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition)


def mail_file(result_file):
    message = Mail(
        from_email='ajayvenkat10@gmail.com',
        to_emails='shankarnarayan91@gmail.com',
        subject='Analysis result',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')

    with open(result_file, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('analysis_result.csv'),
        FileType('text/csv'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    try:
        sg = SendGridAPIClient("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")#os.environ.get('SENDGRID_API_KEY'))
        print(sg)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

# generalized read csv method
def read_csv_file(file_path, delimiter, header_row):
    return pd.read_csv(file_path, sep=delimiter, header=header_row)


# Utility function to slice list of strings by passing start and end values. Returns a set
def string_parser(input_list, start, end):
    for i in range(len(input_list)):
        input_list[i] = str(input_list[i])[start:end]
    return set(input_list)

def float_string_parser(input_list,start,end):
    for i in range(len(input_list)):
        input_list[i] = str(float(input_list[i]))[start:end]
    return set(input_list)

# Pre-processing to remove unwanted rows
def pre_process_merchant_dataframe(merchant_transaction):
    return merchant_transaction.loc[(merchant_transaction["Status of Transaction"] == "Amt. deposited in bank a/c") |
                                    (merchant_transaction["Status of Transaction"] == "Payment Successful") |
                                    (merchant_transaction["Status of Transaction"] == "Settlement In Progress")]


# Initializing map
def set_map_values(intersection):
    intersection = list(intersection)
    map = defaultdict(bool)
    for i in range(len(intersection)):
        map[intersection[i]] = True
    return map


def create_temp_file(suffix="", extension=".csv"):
    file_name = str(uuid.uuid4()) + suffix + extension
    path = os.environ["TMP_FOLDER"]
    return os.path.join(path, file_name)


def download_file_from_url(url):
    r = requests.get(url, allow_redirects=True)

    downloaded_file = create_temp_file()
    with open(downloaded_file, 'wb') as file:
        file.write(r.content)

    return downloaded_file


def get_csv_file_from_url(url):
    return read_csv_file(download_file_from_url(url), ",", 0)


def read_inputs():
    return (read_csv_file(sys.argv[1], ",", 0),
            read_csv_file(sys.argv[2], ",", 0),
            read_csv_file(sys.argv[3], ",", 0))


def write_to_result_file(transactions_in_payu_only, merchant_transaction, checkout_exports, intersection_map):
    
    result_csv = create_temp_file(suffix="_result")
    
    with open(result_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        header_row = ["Payment ID", "User Name", "Transaction ID", "Amount", "Payment Successful On",
                      "Customer Mobile", "Customer E-mail", "Billing Name"]
        writer.writerow(header_row)
    
        for i in range(len(transactions_in_payu_only)):
            # Unable to handle nan cases during pre-processing, hence using a check while processing
            if(transactions_in_payu_only[i] != "n" or transactions_in_payu_only[i] != ""):
                
                row = merchant_transaction.loc[(merchant_transaction["Transaction ID"] == float(
                    transactions_in_payu_only[i])) | (merchant_transaction["Transaction ID"] == int(
                        transactions_in_payu_only[i]))]
                
                # Only a single row is present for each ID as ID is unique, cannot access the row directly +
                # iterator is not required so accessing using iloc
                row_to_write = []

                if(len(row) > 0):
                    for j in range(len(header_row)-1):
                        row_to_write.append(row[header_row[j]].iloc[0])

                    # inner join
                    if(intersection_map[transactions_in_payu_only[i]]):
                        get_row = checkout_exports.loc[checkout_exports["Id"] == float(
                            transactions_in_payu_only[i])]
                        row_to_write.append(get_row["Billing Name"].iloc[0])

                writer.writerow(row_to_write)

    return result_csv


def process_inputs(merchant_transaction, order_exports, checkout_exports):
    merchant_transaction = pre_process_merchant_dataframe(merchant_transaction)

    transaction_id = list(merchant_transaction["Transaction ID"])
    payment_reference = list(order_exports["Payment Reference"])
    notes = list(order_exports["Notes"])
    checkouts_id = list(checkout_exports["Id"])
    
    transaction_id = float_string_parser(transaction_id, 0, -2)
    payment_reference = string_parser(payment_reference, 1, -2)
    checkouts_id = float_string_parser(checkouts_id,0,-2)
    notes = float_string_parser(notes,0,-2)

    transactions_in_payu_only = transaction_id.difference(payment_reference)

    transactions_in_payu_only = list(
        transactions_in_payu_only.difference(notes))

    realised_transactions_with_abandoned_carts = set(
        transactions_in_payu_only) & checkouts_id

    intersection_map = set_map_values(
        realised_transactions_with_abandoned_carts)

    # return write_to_result_file(transactions_in_payu_only,
    #                             merchant_transaction, checkout_exports, intersection_map)

    mail_file(write_to_result_file(transactions_in_payu_only,
                                          merchant_transaction, checkout_exports, intersection_map))

def main():
    merchant_trans, orders_exp, checkouts_exp = read_inputs()
    process_inputs(merchant_trans, orders_exp, checkouts_exp)

if __name__ == "__main__":
    main()
