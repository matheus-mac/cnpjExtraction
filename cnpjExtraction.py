import requests, csv, json

urlBase = "https://consulta-cnpj-gratis.p.rapidapi.com/companies/"
headers = {
    'x-rapidapi-host': "consulta-cnpj-gratis.p.rapidapi.com",
    'x-rapidapi-key': ""
    }

cnpjList  = list()
with open('cnpjrac2.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
        cnpjList.append(row[0])
del cnpjList[0]
print(len(cnpjList))
i = 0
with open("extracaoCNPJ.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    file.write('name;type;founded;size;capital;email;status;city;state;code;description\n') 
    for cnpj in cnpjList:
        i = i + 1
        url = urlBase + cnpj
        response = requests.request("GET", url, headers=headers)
        print(response.text)
        r = json.loads(response.text)
        for key in r.keys():
            if key in ('name','type','founded','size','capital','email','status'):
                #print(list(r.values())[list(r.keys()).index(key)])
                file.write(str(list(r.values())[list(r.keys()).index(key)]) + ";")
            if key in ('registration'):
                registrationDict = list(r.values())[list(r.keys()).index(key)]
                for internKey in registrationDict.keys():
                    if (internKey in 'status'):
                        #print(list(registrationDict.values())[list(registrationDict.keys()).index(internKey)])
                        file.write(str(list(registrationDict.values())[list(registrationDict.keys()).index(internKey)]) + ";")
            if key in ('primary_activity'):
                activityDict = list(r.values())[list(r.keys()).index(key)]
                for internKey in activityDict.keys():
                    if (internKey in ('code','description')):
                        #print(list(activityDict.values())[list(activityDict.keys()).index(internKey)])
                        file.write(str(list(activityDict.values())[list(activityDict.keys()).index(internKey)]) + ";")
            if key in ('address'):
                addressDict = list(r.values())[list(r.keys()).index(key)]
                for internKey in addressDict.keys():
                    if (internKey in ('city','state')):
                        #print(list(addressDict.values())[list(addressDict.keys()).index(internKey)])
                        file.write(str(list(addressDict.values())[list(addressDict.keys()).index(internKey)]) + ";")
        file.write('\n')
        print(i)