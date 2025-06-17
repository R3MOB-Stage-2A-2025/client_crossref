import "./SearchResultsList.css";

//import { useEffect } from "react";
import { SearchResult } from "./SearchResult";


export const SearchResultsList = ({ results }) => {
    const items = results?.message?.items ?? [];

    return (
        <div className="results-list">
            {items.map((item, idx) => (
                <SearchResult key={item.DOI || idx} item={item} />
            ))}
        </div>
    );
};

