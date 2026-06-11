import requests
from xml.dom.minidom import parseString

url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

headers = {
    "Content-Type": "text/xml; charset=utf-8"
}

opcao = 0

while opcao != 4:

    print("\n=== MENU ===")
    print("1 - Código telefônico do país")
    print("2 - Código ISO do país")
    print("3 - Capital do país")
    print("4 - Sair")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        country_code = input("Digite o código ISO do país (BR, US, FR...): ")

        payload = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <CountryIntPhoneCode xmlns="http://www.oorsprong.org/websamples.countryinfo">
                    <sCountryISOCode>{country_code}</sCountryISOCode>
                </CountryIntPhoneCode>
            </soap:Body>
        </soap:Envelope>
        """

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            resultado = parseString(response.text)\
                .getElementsByTagName("m:CountryIntPhoneCodeResult")[0]\
                .firstChild.nodeValue

            print(f"Código telefônico: +{resultado}")

    elif opcao == 2:
        country_name = input("Digite o nome do país: ")

        payload = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <CountryISOCode xmlns="http://www.oorsprong.org/websamples.countryinfo">
                    <sCountryName>{country_name}</sCountryName>
                </CountryISOCode>
            </soap:Body>
        </soap:Envelope>
        """

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            resultado = parseString(response.text)\
                .getElementsByTagName("m:CountryISOCodeResult")[0]\
                .firstChild.nodeValue

            print(f"Código ISO: {resultado}")

    elif opcao == 3:
        country_code = input("Digite o código ISO do país: ")

        payload = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <CapitalCity xmlns="http://www.oorsprong.org/websamples.countryinfo">
                    <sCountryISOCode>{country_code}</sCountryISOCode>
                </CapitalCity>
            </soap:Body>
        </soap:Envelope>
        """

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            resultado = parseString(response.text)\
                .getElementsByTagName("m:CapitalCityResult")[0]\
                .firstChild.nodeValue

            print(f"Capital: {resultado}")

    elif opcao == 4:
        print("Encerrando programa...")

    else:
        print("Opção inválida!")