import "./SearchResult.css";

export const SearchResult = ({ item }) => {
    const title = item.title?.[0] || "Untitled";
    const doi = item.DOI || "No DOI";
    const url = item.URL || `https://doi.org/${doi}`;

    const authors = item.author?.map((a) =>
        [a.given, a.family].filter(Boolean).join(" ")
    ).join(", ") || "No authors";

    const abstract = item.abstract
        ? item.abstract.replace(/<\/?jats:[^>]+>/g, '')
        : "No abstract available";

    return (
        <div className="search-result">
            <h3>{title}</h3>
            <p><strong>DOI:</strong> <a href={url} target="_blank" rel="noopener noreferrer">{doi}</a></p>
            <p><strong>Authors:</strong> {authors}</p>
            <p><strong>Abstract:</strong> {abstract}</p>
        </div>
    );
};

