import { useState, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math"; // ✅ Add support for math
import remarkBreaks from "remark-breaks";
import rehypeRaw from "rehype-raw";
import rehypeKatex from "rehype-katex"; // ✅ Add Katex for math rendering
import "katex/dist/katex.min.css"; // ✅ Import Katex styles
import { Accordion, Message, Loader, Panel } from "rsuite";
import "@/styles/components/Markdown.scss";

const MarkdownFetcher = ({ filename }) => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("MarkdownFetcher filename:", filename);
    if (!filename) {
      setError("No filename provided");
      setLoading(false);
      return;
    }

    const fetchMarkdown = async () => {
      try {
        const apiUrl = `${import.meta.env.VITE_API_BASE_URL}/api/markdown/${filename}`;
        console.log("Fetching markdown from:", apiUrl);
    
        if (!filename) {
          throw new Error("No filename provided.");
        }
    
        const response = await axios.get(apiUrl);
    
        if (response.status === 200) {
          setContent(response.data.content || "No content found.");
        }
      } catch (err) {
        if (err.response && err.response.status === 404) {
          console.error("Markdown file not found:", filename);
          setError("Markdown file not found.");
        } else {
          console.error("Error fetching markdown:", err);
          setError("Failed to load content.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchMarkdown();
  }, [filename]);

  if (loading) return <Loader center content="Loading markdown..." />;
  if (error) return <Message type="error">{error}</Message>;

  return (
    <div className="markdown">
      <Accordion expand="true">

        <Panel bordered header="Definition" defaultExpanded>
          {content ? (
            <div className="markdown-body">
               <ReactMarkdown
                  children={content}
                  remarkPlugins={[remarkGfm, remarkMath, remarkBreaks]}
                  rehypePlugins={[rehypeKatex, rehypeRaw]}
                  components={{
                    math: ({ value }) => <div className="math-block">{value}</div>,
                    inlineMath: ({ value }) => <span className="math-inline">{value}</span>,
                  }}
                />
            </div>
          ) : (
            <div>
              <p>No content found.</p>
            </div>
          )}
        </Panel>
      </Accordion>
    </div>
  );
};

export default MarkdownFetcher;
