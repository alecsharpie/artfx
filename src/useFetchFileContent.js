import { useState, useEffect } from "react";


function useFetchFileContent(url) {
    const [fileContent, setFileContent] = useState("");

    useEffect(() => {
        async function fetchFileContent() {
            const response = await fetch(url);
            const content = await response.text();
            setFileContent(content);
        }
        fetchFileContent();
    }, [url]);

    return fileContent;
}

export default useFetchFileContent;