import { useState, useEffect } from "react";
import { Form, Button, Message, Input } from "rsuite";
import axios from "axios";

const DynamicForm = ({ schema }) => {
  const [formData, setFormData] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [response, setResponse] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Debugging: Check if schema is properly received
  useEffect(() => {
    console.log("DynamicForm received schema:", schema);
  }, [schema]);

  // Ensure schema is properly loaded
  if (!schema) {
    return <p>Error: Schema not loaded.</p>;
  }

  if (!schema.fields || !Array.isArray(schema.fields)) {
    return <p>Error: Invalid schema format. Expected an array of fields.</p>;
  }

  // Debugging: Check schema method
  useEffect(() => {
    console.log("Schema method:", schema.method);
  }, [schema]);

  // Handle form field changes
  const handleChange = (value, field) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  // Convert comma-separated values into an array of numbers
  const handleCommaSeparatedInput = (value, field) => {
    const numberArray = value
      .split(",")
      .map((num) => parseFloat(num.trim())) // Convert to float
      .filter((num) => !isNaN(num)); // Remove invalid values

    setFormData((prev) => ({ ...prev, [field]: numberArray }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setResponse(null);
    setErrorMessage(null);

    try {
      if (!schema.method) {
        throw new Error("Method is missing in schema.");
      }

      const payload = {
        method: schema.method, // Ensure method is included
        data: formData
      };

      console.log("Submitting Data:", payload); // Debugging

      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/process`, payload);
      setResponse(response.data);
    } catch (error) {
      console.error("Error processing form:", error);
      setErrorMessage(error.response?.data?.detail || error.message || "Error submitting form.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Form>
      {schema.fields.map((field) => (
        <Form.Group key={field.name}>
          <Form.ControlLabel>{field.label}</Form.ControlLabel>

          {/* Handle comma-separated input if field is type array */}
          {field.type === "array" ? (
            <Input
              type="text"
              placeholder="Enter numbers separated by commas"
              onChange={(value) => handleCommaSeparatedInput(value, field.name)}
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

      {/* Display API Response */}
      {response && (
        <Message type="success" className="mt-2">
          {response.message} <br />
          <strong>Result:</strong> {JSON.stringify(response.result)}
        </Message>
      )}

      {/* Display Error Message */}
      {errorMessage && (
        <Message type="error" className="mt-2">
          {errorMessage}
        </Message>
      )}
    </Form>
  );
};

export default DynamicForm;
