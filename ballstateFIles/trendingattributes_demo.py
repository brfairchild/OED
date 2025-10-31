from apicall import *
import pandas as pd
from urllib3 import response
import json

site = NULL

loginUrl = site + "/login"

token = fetch_api_key(loginUrl, NULL, NULL)

''' set up and send api query '''
fqr="Metasys15:NAE-47/ModbusTCP.HEALTH PROFESSIONS.HBPM17.APT.Totalization1"
objectId=fqr_to_object(site,fqr,token)
startDate="2025-01-01T00:00:00.000Z"
endDate="2026-01-01T00:00:00.000Z"
yearlyTotalizationUrl=f"{site}/objects/{objectId}/attributes/85/samples"
arguments=f"startTime={startDate}&endTime={endDate}&page=1&pageSize=10000&sort=timestamp"
api_response=fetch_api_value(yearlyTotalizationUrl,token,arguments)

''' output results '''
print(f"{yearlyTotalizationUrl}?{arguments}")
header = {
    "FQR": fqr,
    "Id": objectId,
    "StartDate": startDate,
    "EndDate": endDate
}
print(header)

''' convert to dataframe and write to file '''
headerDF = pd.DataFrame({"name":header.keys(), "Object":header.values()})
hourly=[]
if "OK" in api_response.reason:
    returnData=api_response.json()["items"]
    for hour in returnData:
        thisHour = hour["value"]
        thisHour["timestamp"] = hour["timestamp"]
        hourly.append(thisHour)
    values = pd.DataFrame(hourly)
    trendedValues =pd.concat([headerDF, values],ignore_index=True)
    print(trendedValues.head())
    trendedValues.to_csv(f"healthprof_{startDate}.csv")
else:
    print(api_response.reason)
