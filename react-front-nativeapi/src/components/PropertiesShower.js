import React, { useState, useEffect, process } from "react";
import axios from "axios";

// const baseUrl = `${process.env.REACT_APP_API_URL}/properties/`

function Header({ moleculeName, searchType }) {
    const [expandedKey, setExpandedKey] = useState(null);
    const [statusCode, setStatusCode] = useState(0);
    const [showName, setShowName] = useState(null);
    const [showImage, setShowImage] = useState(null);
    const [properties, setProperties] = useState({});
    const [cid, setCID] = useState(null);

    useEffect(() => {

        const performApiRequest = () => {
            if (moleculeName) {
                const searchTypeAsText = searchType ? "smiles" : "name";

                axios.get(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/${searchTypeAsText}/${moleculeName}/cids/json`).then(
                    (response) => {
                        setStatusCode(200);

                        setCID(response.data.IdentifierList.CID[0])
                        console.log(response.data.IdentifierList.CID[0])
                        setShowImage(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${response.data.IdentifierList.CID[0]}/PNG`)

                        axios.get(
                            `https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/${response.data.IdentifierList.CID[0]}/JSON/`
                        ).then(
                            (response) => {
                                setShowName(response.data.Record.RecordTitle)
                                console.log(response.data.Record.Section)


                                response.data.Record.Section.forEach(function (section) {
                                    if (section["TOCHeading"] === "Chemical and Physical Properties") {
                                        section["Section"].forEach(function (subsection) {
                                            if (subsection["TOCHeading"] === "Computed Properties" || subsection["TOCHeading"] === "Experimental Properties") {
                                                subsection["Section"].forEach(function (subsubsection) {
                                                    var subsubsection_val;
                                                    if ("Value" in subsubsection) {
                                                        subsubsection_val = "Value";
                                                    } else {
                                                        subsubsection_val = "Information";
                                                    }
                                                    properties[subsubsection["TOCHeading"]] = [];
                                                    subsubsection[subsubsection_val].forEach(function (information) {
                                                        try {
                                                            if ("StringWithMarkup" in information["Value"]) {
                                                                if (!properties[subsubsection["TOCHeading"]].includes(information["Value"]["StringWithMarkup"][0]["String"]))
                                                                properties[subsubsection["TOCHeading"]].push(information["Value"]["StringWithMarkup"][0]["String"]);
                                                            } else {
                                                                properties[subsubsection["TOCHeading"]].push(information["Value"]["Number"][0]);
                                                            }
                                                        } catch (error) {
                                                            
                                                        }
                                                    });
                                                });
                                            }
                                        });
                                    }
                                });


                            }
                        )
                    }
                ).catch((error) => {
                    setStatusCode(error.response.status)
                })

                // if(statusCode === 200) {
                //     console.log(cid)
                //     axios.get(
                //         `https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/${cid}/JSON/`
                //     ).then(
                //         (response) => {
                //             setShowName(response.data.Record.RecordTitle)
                //         }
                //     )
                // }

                // const request = `${baseUrl}${searchTypeAsText}/${moleculeName}`;
                // axios.get(request).then((response) => {
                //     setStatusCode(200);
                //     setShowName(response.data.Name);
                //     setShowImage(response.data.Image);
                //     setProperties(response.data.Properties);
                // }).catch((error) => {
                //     setStatusCode(error.response.status);
                // });
            }
        };

        performApiRequest();
    }, [moleculeName, searchType]);

    function toggleExpand(key) {
        setExpandedKey(prevKey => prevKey === key ? null : key);
    }


    if (statusCode === 200) {
        return (
            <div>
                <img src={showImage} alt="structure"></img>
                <header className="header">
                    <p>{showName}</p>
                </header>
                {Object.entries(properties).map(([key, value]) => (
                    <div key={key}>
                        <button onClick={() => toggleExpand(key)}>
                            {key}
                        </button>
                        {
                        expandedKey === key && <div className="properies">{
                            value.map((val, ind) => (
                                <p className="properies_value" key={ind}>{val}</p>
                            ))
                        }</div>}
                    </div>
                ))}
            </div>
        );
    }
    if (statusCode === 404) {
        return (
            <header className="header">
                No such structure.
            </header>
        )
    }
    if (statusCode === 400) {
        return (
            <header className="header">
                Wrong representation.
            </header>
        )
    }
    return (
        <header className="header">
            Select molecule.
        </header>
    )
}


export default Header;
