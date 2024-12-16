import requests

url = "https://data.tmd.go.th/api/Weather3Hours/V2/?uid=api&ukey=api12345&format=json"

response = requests.get(url).json()
data = response["Stations"]["Station"]

keyword = input("ใส่สถานีที่ต้องการ: ")
for x in data:
    if keyword in x["StationNameThai"]:
        staName = x["StationNameThai"]
        airTemp = x["Observation"]["AirTemperature"]
        print(staName, airTemp)
