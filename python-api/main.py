from fastapi import FastAPI, HTTPException
import requests
from typing import Literal
import aiohttp
import asyncio

client = aiohttp.ClientSession()

app = FastAPI()

# async def get_request(url):
#     async with session.get(url) as resp:
#         pokemon = await resp.json()
#         return pokemon['name']


@app.get("/properties_from_cid/{cid}")
async def get_properties_from_cid(cid: int) -> dict:
    request = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/")
    # request = await client.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/")
    data = request.json()
    # data = await request.json(encoding="utf-8")
    del request
    response = {}
    response["CID"] = cid
    response["Name"] = data["Record"]["RecordTitle"]
    response["Image"] = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
    response["Properties"] = {}
    for section in data["Record"]["Section"]:
        if section["TOCHeading"] in ("Chemical and Physical Properties"):
            for subsection in section["Section"]:
                if subsection["TOCHeading"] in ("Computed Properties", "Experimental Properties"):
                    for subsubsection in subsection["Section"]:
                        if "Value" in subsubsection:
                            subsubsection_val = "Value"
                        else:
                            subsubsection_val = "Information"
                        response["Properties"][subsubsection["TOCHeading"]] = []
                        for information in subsubsection[subsubsection_val]:
                            try:
                                if "StringWithMarkup" in information["Value"]:
                                    response["Properties"][subsubsection["TOCHeading"]].append(information["Value"]["StringWithMarkup"][0]["String"])
                                else:
                                    response["Properties"][subsubsection["TOCHeading"]].append(information["Value"]["Number"][0])
                            except:
                                pass
    return response

@app.get("/properties/{nametype}/{name}")
async def get_properties(nametype: Literal["name", "smiles", "cid"], name: str):
    # response = await client.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{nametype}/{name}/cids/json")
    response = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{nametype}/{name}/cids/json")
    # data = await response.json()
    data = response.json()
    # match response.status:
    match response.status_code:
        case 200:
            cid = data["IdentifierList"]["CID"][0]
            return await get_properties_from_cid(cid)
        case 400:
            raise HTTPException(status_code=400, detail="Проверьте, правильно ли выбран тип поиска и название.")
        case 404:
            raise HTTPException(status_code=404, detail="Нет вещества по заданному названию.")
        
