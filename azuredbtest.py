from AzureDB import AzureDB
#AzureDB().azureAddData()
#AzureDB().azureDeleteData()
with AzureDB() as a:
    data = a.azureGetData()
    for result in data:
        print("%s napisal: \"%s\""%(result['name'], result['text']))