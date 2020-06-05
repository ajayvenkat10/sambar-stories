import abc

class PaymentServiceProvider(abc.ABC):

    provider_transactions = set()
    
    def __init__(self, provider_csv):
        self.provider_csv = provider_csv

    def setProviderTransactions(self, provider_transactions):
        self.provider_transactions = provider_transactions

    def getProviderTransactions(self):
        return self.provider_transactions

    def getProviderCSV(self):
        return self.provider_csv

    def parseDataInField(self, input_list, start, end):
        for i in range(len(input_list)):
            input_list[i] = str(float(input_list[i]))[start:end]
        return set(input_list)

    @abc.abstractmethod
    def preProcessData(self):
        pass
    


    

