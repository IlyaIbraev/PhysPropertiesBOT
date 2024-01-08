import React, { useState, useEffect, process } from "react";
import axios from "axios";

const baseUrl = `${process.env.REACT_APP_API_URL}/properties/`

function Header({ moleculeName, searchType }) {
    const [expandedKey, setExpandedKey] = useState(null);
    const [statusCode, setStatusCode] = useState(null);
    const [showName, setShowName] = useState(null);
    const [showImage, setShowImage] = useState(null);
    const [properties, setProperties] = useState(null);
    
    useEffect(() => {
        
        const performApiRequest = () => {
            if (moleculeName) {
                const searchTypeAsText = searchType ? "smiles" : "name";
                const request = `${baseUrl}${searchTypeAsText}/${moleculeName}`;
                axios.get(request).then((response) => {
                    setStatusCode(200);
                    setShowName(response.data.Name);
                    setShowImage(response.data.Image);
                    setProperties(response.data.Properties);
                }).catch((error) => {
                    setStatusCode(error.response.status);
                });
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
                        {expandedKey === key && <div className="properies">{
                            value.map((val) => (
                                <p className="properies_value" key={val}>{val}</p>
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
