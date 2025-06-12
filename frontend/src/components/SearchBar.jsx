import "./SearchBar.css";

import { useState, useEffect } from "react";
import { FaSearch } from "react-icons/fa";

import { socket } from "../socket";

export const SearchBar = ({ setResults }) => {
    const [input, setInput] = useState("");

    useEffect(() => {
        socket.on("search_results", (data) => {
            setResults(data.results);
        });

        return () => {
            socket.off("search_results");
        };
    }, [setResults]);

    const handleChange = (value) => {
        setInput(value);
        socket.emit("search_query", value);
    };

    return (
        <div className="input-wrapper">
            <FaSearch id="search-icon" />
            <input
                placeholder="Type to search..."
                value={input}
                onChange={(e) => handleChange(e.target.value)}
            />
        </div>
    );
};

