from fastapi import FastAPI, HTTPException
import requests
from typing import Literal

app = FastAPI()

@app.get("/properties_from_cid/{cid}")
def get_properties_from_cid(cid: int) -> dict:
    response = {}
    request = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/")
    for section in request.json()["Record"]["Section"]:
        if section["TOCHeading"] in ("Chemical and Physical Properties"):
            for subsection in section["Section"]:
                if subsection["TOCHeading"] in ("Computed Properties", "Experimental Properties"):
                    for subsubsection in subsection["Section"]:
                        if "Value" in subsubsection:
                            subsubsection_val = "Value"
                        else:
                            subsubsection_val = "Information"
                        response[subsubsection["TOCHeading"]] = []
                        for information in subsubsection[subsubsection_val]:
                            if "StringWithMarkup" in information["Value"]:
                                response[subsubsection["TOCHeading"]].append(information["Value"]["StringWithMarkup"][0]["String"])
                            else:
                                response[subsubsection["TOCHeading"]].append(information["Value"]["Number"][0])
    return response

@app.get("/properties/{nametype}/{name}")
def get_properties(nametype: Literal["name", "smiles"], name: str):
    response = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{nametype}/{name}/cids/json")
    match response.status_code:
        case 200:
            cid = response.json()["IdentifierList"]["CID"][0]
            return get_properties_from_cid(cid)
        case 400:
            return HTTPException(status_code=400, detail="Проверьте, правильно ли выбран тип поиска и название.")
        case 404:
            return HTTPException(status_code=404, detail="Нет вещества по заданному названию.")
        
