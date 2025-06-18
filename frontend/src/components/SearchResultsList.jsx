import "./SearchResultsList.css";

//import { useEffect } from "react";
import { SearchResult } from "./SearchResult";


export const SearchResultsList = ({ results, loading, setLoading }) => {
    const items = results?.['message']?.['items'] ?? [];

    return (
        <div className="results-list">
            {items.map((item) => (
                <SearchResult
                    item={item}
                    loading={loading}
                    setLoading={setLoading}
                />
            ))}
        </div>
    );
};

