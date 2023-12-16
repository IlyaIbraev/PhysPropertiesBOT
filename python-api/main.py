from fastapi import FastAPI
import requests

app = FastAPI()

BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compond/"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/cid_from_name/{name}")
def get_cid_from_name(name: str):
    result = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/json")
    return result.json()

@app.get("/properties_from_cid/{cid}")
def get_properties_from_cid(cid: int):
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