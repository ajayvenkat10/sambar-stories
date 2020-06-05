from PaymentServiceProvider import *

class PayU(PaymentServiceProvider):

    TRANSACTION_ID = "Transaction ID"
    STATUS_OF_TRANSACTION = "Status of Transaction"

    def __init__(self, provider_csv):
        super().__init__(provider_csv)
        self.preProcessData()

    def preProcessData(self):
        self.provider_csv = self.provider_csv.loc[
            (self.provider_csv[self.STATUS_OF_TRANSACTION] == "Amt. deposited in bank a/c") |
            (self.provider_csv[self.STATUS_OF_TRANSACTION] == "Payment Successful") |
            (self.provider_csv[self.STATUS_OF_TRANSACTION] == "Settlement In Progress")]
        self.setData()

    def setData(self):
        self.setProviderTransactions(self.parseDataInField(
            list(self.provider_csv[self.TRANSACTION_ID]), 0, -2))
