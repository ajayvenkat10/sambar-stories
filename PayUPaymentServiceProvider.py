class PayUPaymentServiceProvider:

    TRANSACTION_ID = "Transaction ID"
    STATUS_OF_TRANSACTION = "Status of Transaction"

    def __init__(self, merchant_transaction):
        self.merchant_transaction = merchant_transaction
        self.preProcessData()

    def preProcessData(self):
        self.merchant_transaction = self.merchant_transaction.loc[
                    (self.merchant_transaction[self.STATUS_OF_TRANSACTION] == "Amt. deposited in bank a/c") |
                    (self.merchant_transaction[self.STATUS_OF_TRANSACTION] == "Payment Successful") |
                    (self.merchant_transaction[self.STATUS_OF_TRANSACTION] == "Settlement In Progress")]
        self.setTransactionId()

    def setTransactionId(self):
        self.transaction_id = self.parseTransactionId(
            list(self.merchant_transaction[self.TRANSACTION_ID]), 0, -2)

    def getTransactionId(self):
        return self.transaction_id

    def getMerchantTransaction(self):
        return self.merchant_transaction

    def parseTransactionId(self, input_list, start, end):
        for i in range(len(input_list)):
            input_list[i] = str(float(input_list[i]))[start:end]
        return set(input_list)

    
