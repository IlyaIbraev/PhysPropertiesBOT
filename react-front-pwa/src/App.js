// import React from 'react';
// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

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
