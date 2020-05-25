from collections import defaultdict
import math
import csv
import sys
import numpy as np
import pandas as pd

# generalized read csv method  
def read_csv_file(file_path, delimiter, header_row):
    return pd.read_csv(file_path, sep=delimiter, header=header_row)

# Utility function to slice strings by passing start and end values 
def string_parser(input_list, start, end):
    for i in range(len(input_list)):
        input_list[i] = str(input_list[i])[start:end]
    return input_list

# Pre-processing to remove unwanted rows 
def pre_process_merchant_dataframe():
    return merchant_transaction.loc[(merchant_transaction["Status of Transaction"] == "Amt. deposited in bank a/c") |
                                    (merchant_transaction["Status of Transaction"] == "Payment Successful") |
                                    (merchant_transaction["Status of Transaction"] == "Settlement In Progress")]

# Initializing map 
def set_map_values(intersection):
    intersection = list(intersection)

    for i in range(len(intersection)):
        intersection_map[intersection[i]] = True

merchant_transaction = read_csv_file(
    "D:\\Sambar Stories\\merchant_transaction_file.csv", ",", 0)
order_exports = read_csv_file(
    "D:\\Sambar Stories\\order_exports_file.csv", ",", 0)
checkout_exports = read_csv_file(
    "D:\\Sambar Stories\\checkout_exports.csv", ",", 0)

merchant_transaction = pre_process_merchant_dataframe()

transaction_id = list(merchant_transaction["Transaction ID"])
payment_reference = list(order_exports["Payment Reference"])
checkouts_id = list(checkout_exports["Id"])

transaction_id = string_parser(transaction_id, 0, -2)
payment_reference = string_parser(payment_reference, 1, -2)
checkouts_id = string_parser(checkouts_id, 0, -2)

transaction_id = set(transaction_id)
payment_reference = set(payment_reference)
checkouts_id = set(checkouts_id)

transactions_in_payu_only = list(transaction_id.difference(payment_reference))
realised_transactions_with_abandoned_carts = set(transactions_in_payu_only) & checkouts_id

intersection_map = defaultdict(bool)
set_map_values(realised_transactions_with_abandoned_carts)

with open("transactions_in_payu_but_not_in_shopify.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Payment ID", "User Name", "Transaction ID", "Amount", "Payment Successful On",
                     "Customer Mobile", "Customer E-mail", "Billing Name"])

    for i in range(len(transactions_in_payu_only)):
        if(transactions_in_payu_only[i] != "n"):                     # Unable to handle nan cases during pre-processing, hence using a check while processing 
            row = merchant_transaction.loc[merchant_transaction["Transaction ID"] == float(
                transactions_in_payu_only[i])]

            # Only a single row is present for each ID as ID is unique, cannot access the row directly + iterator is not required so accessing using iloc
            row_to_write = [row["Payment ID"].iloc[0], row["User Name"].iloc[0], row["Transaction ID"].iloc[0], row["Amount"].iloc[0],
                                row["Payment Successful On"].iloc[0], row["Customer Mobile"].iloc[0], row["Customer E-mail"].iloc[0]]

            # inner join 
            if(intersection_map[transactions_in_payu_only[i]]):
                get_row = checkout_exports.loc[checkout_exports["Id"] == float(transactions_in_payu_only[i])]
                row_to_write.append(get_row["Billing Name"].iloc[0])
            
            writer.writerow(row_to_write)
