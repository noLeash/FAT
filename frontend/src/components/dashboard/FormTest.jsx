import { useState, useEffect } from "react";
import { fetchSchema } from "../../api/schema";
import { Input, InputGroup, Button } from "rsuite";
import axios from "axios";
import "@/styles/components/Inputs.scss"

const FormTest = ( schema ) => {
    // const [schema, setSchema] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState({}); // Store input values
    const [submitting, setSubmitting] = useState(false);
    const [response, setResponse] = useState(null);
    const [errorMessage, setErrorMessage] = useState(null);

    // useEffect(() => {
    //     const loadSchema = async () => {
    //         try {
    //             const data = await fetchSchema("schema");
    //             console.log("Schema Test received schema:", data);
    //             setSchema(data);
                
    //             // Initialize formData with empty values
    //             const initialFormData = {};
    //             data?.fields?.forEach((field) => {
    //                 initialFormData[field.name] = ""; // Default value
    //             });
    //             setFormData(initialFormData);
    //         } catch (err) {
    //             setError("Failed to load schema");
    //         } finally {
    //             setLoading(false);
    //         }
    //     };
    //     loadSchema();
    // }, []);

    // Handle input changes
    const handleInputChange = (fieldName, value) => {
        setFormData((prev) => ({
            ...prev,
            [fieldName]: value, // Update specific field
        }));
    };

    // Handle form submission
    const handleSubmit = async () => {
        alert(`Submitted values: ${JSON.stringify(formData, null, 2)}`);
        console.log("Submitted values:", formData);
        
        setSubmitting(true);
        setResponse(null);
        setErrorMessage(null);
    
        try {
            if (!schema?.method) throw new Error("Method is missing in schema.");
    
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

    if (error) return <p>{error}</p>;

    return (
        <div className="inputs">
            <h3>{schema.title}:</h3>
            <div>
                {schema?.fields?.map((field) => (
                    <div key={field.name}>
                        <div className="inputs__title">
                            {field.name /* ({field.type}) */}
                        </div>
                        {field.type === "pct" ? (
                            <InputGroup inside style={{ width: 200 }}>
                                <Input
                                    placeholder={field.name}
                                    value={formData[field.name] || ""}
                                    onChange={(value) => handleInputChange(field.name, value)}
                                />
                                <InputGroup.Addon>%</InputGroup.Addon>
                            </InputGroup>
                        ) : field.type === "float" ? (
                            <InputGroup inside style={{ width: 200 }}>
                                <Input
                                    placeholder="XX.XX"
                                    value={formData[field.name] || ""}
                                    onChange={(value) => handleInputChange(field.name, value)}
                                />
                                <InputGroup.Addon>%</InputGroup.Addon>
                            </InputGroup>
                        ) : field.type === "num_pct_pair" ? (
                            <InputGroup inside style={{ width: 200 }}>
                                <Input
                                    placeholder="numPctPair"
                                    value={formData[field.name] || ""}
                                    onChange={(value) => handleInputChange(field.name, value)}
                                />
                                <InputGroup.Addon>%</InputGroup.Addon>
                            </InputGroup>
                        ) : (
                            <InputGroup inside style={{ width: 200 }}>
                                <Input
                                    placeholder="other"
                                    value={formData[field.name] || ""}
                                    onChange={(value) => handleInputChange(field.name, value)}
                                />
                                <InputGroup.Addon>%</InputGroup.Addon>
                            </InputGroup>
                        )}
                    </div>
                ))}
                <Button
                    appearance="primary"
                    onClick={handleSubmit}
                    style={{ marginTop: "10px" }}
                    disabled={submitting}
                >
                    {submitting ? "Submitting..." : "Submit"}
                </Button>

                

                {response && <p>Response: {JSON.stringify(response.result)}</p>}
                {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
            </div>
        </div>
    );
};

export default FormTest;
