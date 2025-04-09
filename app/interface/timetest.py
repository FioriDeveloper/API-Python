import requests

city =  "São Paulo"
api_url = "https://timeapi.io/api/Time/current/ip?ipAddress=187.255.99.16"

response = requests.get(api_url)


def Gettime ():
    if response.status_code == 200:
        dados = response.json()


        data = dados["date"]
         hora = dados["time"]

        print(f"Data: {data}")
        print(f"Hora: {hora}")

        return data,hora