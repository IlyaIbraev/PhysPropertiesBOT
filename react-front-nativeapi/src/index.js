import { StrictMode } from 'react';
import * as ReactDOMClient from "react-dom/client";
import App from "./App"
import "./css/main.css"

const app = ReactDOMClient.createRoot(document.getElementById("root"));

try {
    app.render(
        <StrictMode>
            <App />
        </StrictMode>
    )
} catch (error) {
    console.error('Failed to render the app', error);

}
