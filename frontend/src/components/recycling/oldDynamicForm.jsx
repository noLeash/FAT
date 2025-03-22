import { useState, useEffect } from "react";
import { Form, Button, Message, Input } from "rsuite";
import axios from "axios";
import ErrorBoundary from "../../api/ErrorBoundary";

const DynamicForm = ({ schema }) => {
  if (!schema || !schema.fields || !Array.isArray(schema.fields)) {
    console.error("Error: Invalid schema format", schema);
    return <p>Error: Invalid schema format.</p>;
  }

  const [formData, setFormData] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [response, setResponse] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    console.log("DynamicForm received schema:", schema);
  }, [schema]);

  const handleChange = (value, field, type) => {
    let parsedValue = value;

    // Handle different input types
    if (type === "comma_list") {
      parsedValue = value.split(",").map((item) => item.trim()); // Convert to array
    } else if (type === "float") {
      parsedValue = parseFloat(value);
      if (isNaN(parsedValue)) parsedValue = ""; // Reset if invalid
    }

    setFormData((prev) => ({ ...prev, [field]: parsedValue }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setResponse(null);
    setErrorMessage(null);

    try {
      if (!schema.method) throw new Error("Method is missing in schema.");

      const payload = {
        method: schema.method,
        data: formData,
      };

      console.log("Submitting Data:", payload);

      const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/api/process`,
        payload
      );
      console.log("API Response from Process:", response.data);

      setResponse(response.data);
    } catch (error) {
      console.error("Error processing form:", error);
      setErrorMessage(
        error.response?.data?.detail || error.message || "Error submitting form."
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <ErrorBoundary>
      <Form>
        {schema.fields.map((field) => (
          <Form.Group key={field.name}>
            <Form.ControlLabel>{field.label}</Form.ControlLabel>

            {field.type === "markdown" ? (
              <Input
                as="textarea"
                rows={5}
                placeholder="Enter markdown content"
                onChange={(value) => handleChange(value, field.name, "markdown")}
              />
            ) : field.type === "comma_list" ? (
              <Input
                placeholder="Enter comma-separated values"
                onChange={(value) => handleChange(value, field.name, "comma_list")}
              />
            ) : field.type === "float" ? (
              <Input
                type="number"
                step="any"
                placeholder="Enter a float value"
                onChange={(value) => handleChange(value, field.name, "float")}
              />
            ) : (
              <Form.Control
                name={field.name}
                type={field.type || "text"}
                onChange={(value) => handleChange(value, field.name)}
              />
            )}
          </Form.Group>
        ))}

        <Button appearance="primary" onClick={handleSubmit} disabled={submitting}>
          {submitting ? "Submitting..." : "Submit"}
        </Button>

        {errorMessage && (
          <Message type="error" className="mt-2">
            {errorMessage}
          </Message>
        )}
      </Form>
    </ErrorBoundary>
  );
};

export default DynamicForm;
