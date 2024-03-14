import os
import csv
from os import walk
from bs4 import BeautifulSoup
import re

print("Iniciando processamento de notas fiscais.")

files = []
for (dirpath, dirnames, filenames) in walk(os.getcwd()):
    files.extend(filenames)
    break

rows = ['produto', 'ncm', 'unidade', 'quantidade', 'valorUnidade',
        'valorProduto', 'destCNPJ/destCPF', 'comprador', 'dataEmissao']
dataList = [rows]

for xml in files:
    if("xml" in xml):
        with open(xml, 'r', encoding="UTF-8", errors="ignore") as file:
            print("Processando", xml)
            data = file.read()
            soup = BeautifulSoup(data, 'lxml')
            products = soup.find_all('prod')
            def check_cnpj(self):
                    cnpj = soup.find('dest').find('cnpj')
                    if cnpj:
                        return 'cnpj'
                    else:
                        return 'cpf'
            for product in products:
                try:
                    dataList.append([product.find('xprod').getText(),
                                 product.find('ncm').getText(),
                                 product.find('ucom').getText(),
                                 re.sub(r'\.', ',',product.find('qcom').getText()),
                                 re.sub(r'\.', ',',product.find('vuncom').getText()),
                                 re.sub(r'\.', ',', product.find('vprod').getText()),
                                 soup.find('dest').find(check_cnpj).getText(),
                                 soup.find('dest').find('xnome').getText(),
                                 soup.find('dhemi').getText()])
                except Exception as e:
                    print({xml},repr(e))
                except:
                    pass

with open('vendas.csv', 'w', newline='') as csvFile:
    write = csv.writer(csvFile, delimiter=";")
    write.writerows(dataList)

print("Processamento finalizado com sucesso")
