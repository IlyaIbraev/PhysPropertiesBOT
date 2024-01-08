import React, { useState } from "react";

function MoleculeSelector({ onSearching }) {
   const [searchType, setSearchType] = useState(false);
   const [moleculeName, setMoleculeName] = useState("");

   const handleSearch = (e) => {
       e.preventDefault();
       onSearching(searchType, moleculeName);
   };

   return (
       <div>
           <form onSubmit={handleSearch}>
               <div>
                  <label className="left">Names</label>
                  <label className="toggle">
                      <input type="checkbox" checked={searchType} onChange={(e) => setSearchType(e.target.checked)} />
                      <span className="slider"></span>
                  </label>
                  <label className="right">SMILES</label>
               </div>
               <div>
                  <input
                      type="text"
                      placeholder={searchType ? "SMILES" : "Names"}
                      value={moleculeName}
                      onChange={(e) => setMoleculeName(e.target.value)}
                  />
                </div>
                <div>
                  <input type="submit" value="Search" />
               </div>
           </form>
       </div>
   );
}

export default MoleculeSelector;
