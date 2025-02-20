import { useState, useEffect } from "react";
import DynamicForm from "./DynamicForm";
import { Card, CardContent } from "../ui/card";
import { fetchSchema } from "../../api/schema";
import MarkdownViewer from "../ui/MarkdownViewer";

const MethodBox = ({ method }) => {
  const [schema, setSchema] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadSchema = async () => {
      try {
        const data = await fetchSchema(method);
        console.log("MethodBox received schema:", data);
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

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <Card className="p-4">
      <h2 className="text-xl font-bold mb-4">{schema?.title}</h2>
      <DynamicForm schema={schema} />
      {schema?.markdown && <MarkdownViewer file={schema.markdown} />}
    </Card>
  );
};

export default MethodBox;
