import aiohttp
from fastapi import FastAPI, HTTPException
import requests
from typing import Literal
import asyncpg
import json

app = FastAPI()


@app.get("/properties_from_cid/{cid}")
async def get_properties_from_cid(cid: int) -> dict:
    conn = await asyncpg.connect('postgresql://postgres:password@localhost/pubchem')
    await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
    # try:
    #     await conn.execute('''
    #         DROP TABLE properties
    #     ''')
    #     await conn.execute('''
    #         CREATE TABLE properties(
    #                 cid serial,
    #                 data json
    #         )
    #     ''')
    # except:
    #     pass
    
    data = await conn.fetchval('SELECT data FROM properties WHERE cid=$1', cid)
    if data:
        return data

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/",
        ) as response:
            data = await response.json(encoding="CP866")
    output_data = {}
    output_data["CID"] = cid
    output_data["Name"] = data["Record"]["RecordTitle"]
    output_data["Image"] = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
    output_data["Properties"] = {}
    for section in data["Record"]["Section"]:
        if section["TOCHeading"] in ("Chemical and Physical Properties"):
            for subsection in section["Section"]:
                if subsection["TOCHeading"] in ("Computed Properties", "Experimental Properties"):
                    for subsubsection in subsection["Section"]:
                        if "Value" in subsubsection:
                            subsubsection_val = "Value"
                        else:
                            subsubsection_val = "Information"
                        output_data["Properties"][subsubsection["TOCHeading"]] = []
                        for information in subsubsection[subsubsection_val]:
                            try:
                                if "StringWithMarkup" in information["Value"]:
                                    output_data["Properties"][subsubsection["TOCHeading"]].append(information["Value"]["StringWithMarkup"][0]["String"])
                                else:
                                    output_data["Properties"][subsubsection["TOCHeading"]].append(information["Value"]["Number"][0])
                            except:
                                pass

    await conn.execute('''
        INSERT INTO properties(cid, data) VALUES($1, $2::json)
    ''', cid, output_data)
    return output_data

@app.get("/properties/{nametype}/{name}")
async def get_properties(nametype: Literal["name", "smiles", "cid"], name: str):
    
    if nametype == "cid":
        return await get_properties_from_cid(int(name))

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{nametype}/{name}/cids/json") as response:
            data = await response.json(encoding="Windows-1252")
    match response.status:
        case 200:
            cid = data["IdentifierList"]["CID"][0]
            return await get_properties_from_cid(cid)
        case 400:
            raise HTTPException(status_code=400, detail="Проверьте, правильно ли выбран тип поиска и название.")
        case 404:
            raise HTTPException(status_code=404, detail="Нет вещества по заданному названию.")
        
