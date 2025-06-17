import "./App.css";

import { useState, useEffect } from "react";
import { SearchBar } from "./components/SearchBar";
import { SearchResultsList } from "./components/SearchResultsList";

import { socket } from "./socket";

function App() {
    const [results, setResults] = useState([]);

    useEffect(() => {
        socket.on("search_results", (data) => {
            setResults(data.results);
        });

        return () => {
            socket.off("search_results");
        };
    }, []);

    return (
        <div className="App">
            <div className="search-bar-container">
                <SearchBar setResults={setResults} />
                <SearchResultsList results={results} />
            </div>
        </div>
    );
}

export default App;

