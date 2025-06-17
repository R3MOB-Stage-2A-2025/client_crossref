import "./SearchBar.css";

import { useState, useEffect } from "react";
import { FaSearch } from "react-icons/fa";

import { socket } from "../socket";

export const SearchBar = ({ setResults }) => {
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        socket.on("search_results", (data) => {
            setResults(data.results);
            setLoading(false);
        });

        return () => {
            socket.off("search_results");
        };
    }, [setResults]);

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !loading) {
            setLoading(true);
            socket.emit("search_query", input);
        }
    };

    return (
        <div className="input-wrapper">
            <FaSearch id="search-icon" />
            <input
                placeholder="DOI, Title, Abstract, Author, etc..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
            />
            {loading && <span className="loading">Searching...</span>}
        </div>
    );
};

