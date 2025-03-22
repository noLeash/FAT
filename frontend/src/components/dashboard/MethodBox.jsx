import { useState, useEffect } from "react";
import DynamicForm from "./DynamicForm";
import { Card, Button, Loader, Message, Accordion, Panel } from "rsuite";
import { fetchSchema } from "../../api/schema";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import remarkBreaks from "remark-breaks";
import rehypeRaw from "rehype-raw";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import "@/styles/components/Markdown.scss";

const MethodBox = ({ method, onClose }) => {
  const [schema, setSchema] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [response, setResponse] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // ✅ Markdown State
  const [markdownContent, setMarkdownContent] = useState(null);
  const [markdownLoading, setMarkdownLoading] = useState(false);
  const [markdownError, setMarkdownError] = useState(null);

  useEffect(() => {
    const loadSchema = async () => {
      try {
        const data = await fetchSchema(method);
        setSchema(data);
      } catch (err) {
        setError("Failed to load schema");
      } finally {
        setLoading(false);
      }
    };

    if (method) {
      loadSchema();
    }
  }, [method]);

  // ✅ Fetch Markdown when schema is loaded
  useEffect(() => {
    const fetchMarkdown = async () => {
      if (!schema?.markdown) return;

      setMarkdownLoading(true);
      setMarkdownError(null);
      setMarkdownContent(null);

      try {
        const apiUrl = `${import.meta.env.VITE_API_BASE_URL}/api/markdown/${schema.markdown}`;
        console.log("Fetching markdown from:", apiUrl);
        
        const response = await axios.get(apiUrl);
        setMarkdownContent(response.data.content || "No content found.");
      } catch (err) {
        if (err.response?.status === 404) {
          setMarkdownError("Markdown file not found.");
        } else {
          setMarkdownError("Failed to load markdown content.");
        }
      } finally {
        setMarkdownLoading(false);
      }
    };

    if (schema?.markdown) {
      fetchMarkdown();
    }
  }, [schema?.markdown]);

  const handleInputChange = (fieldName, value) => {
    setFormData((prev) => ({
      ...prev,
      [fieldName]: value,
    }));
  };

  const handleSubmit = async () => {
    if (errorMessage) {
      console.error("Form contains invalid data. Fix errors before submitting.");
      return;
    }

    setSubmitting(true);
    setResponse(null);
    setErrorMessage(null);

    try {
      if (!schema?.method) throw new Error("Method is missing in schema.");

      const payload = {
        method: schema.method,
        data: formData,
      };

      const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/api/process`,
        payload
      );

      setResponse(response.data);
    } catch (error) {
      setErrorMessage(error.response?.data?.detail || error.message || "Error submitting form.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <Card bordered className="methodbox__container">
      <div className="methodbox__header">
        <h2>{schema?.title}</h2>
        <Button appearance="subtle" size="xs" onClick={() => onClose(method)}>
          ✖
        </Button>
      </div>
      
      <DynamicForm
        schema={schema}
        formData={formData} 
        setFormData={setFormData}
        errorMessage={errorMessage}
        setErrorMessage={setErrorMessage}
        handleInputChange={handleInputChange}
        handleSubmit={handleSubmit}
        submitting={submitting}
        response={response}
      />

      {/* ✅ Markdown Section Inside MethodBox */}
      {schema?.markdown && (
        <div className="markdown">
          <Accordion>
            <Panel bordered header="Definition" defaultExpanded>
              {markdownLoading ? (
                <Loader center content="Loading markdown..." />
              ) : markdownError ? (
                <Message type="error">{markdownError}</Message>
              ) : (
                <div className="markdown-body">
                  <ReactMarkdown
                    children={markdownContent}
                    remarkPlugins={[remarkGfm, remarkMath, remarkBreaks]}
                    rehypePlugins={[rehypeKatex, rehypeRaw]}
                    components={{
                      math: ({ value }) => <div className="math-block">{value}</div>,
                      inlineMath: ({ value }) => <span className="math-inline">{value}</span>,
                    }}
                  />
                </div>
              )}
            </Panel>
          </Accordion>
        </div>
      )}
    </Card>
  );
};

export default MethodBox;
