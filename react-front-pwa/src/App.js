import React, { useState } from "react";
import Header from "./components/Header";
import MoleculeSelector from "./components/MoleculeSelector";
import PropertiesShower from "./components/PropertiesShower";

function App() {
   const [searchType, setSearchType] = useState(false);
   const [moleculeName, setMoleculeName] = useState("");

   const getProperties = (searchType, moleculeName) => {
       setSearchType(searchType);
       setMoleculeName(moleculeName);
   };

   return (
       <div>
           <Header />
           <MoleculeSelector onSearching={getProperties} />
           <PropertiesShower searchType={searchType} moleculeName={moleculeName} />
       </div>
   );
}

export default App;


// export default App;
