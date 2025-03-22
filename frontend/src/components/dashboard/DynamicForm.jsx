import { useState, useEffect } from "react";
import { Input, InputGroup, Button, DatePicker } from "rsuite";
import axios from "axios";
import "@/styles/components/Inputs.scss";
import ErrorBoundary from "../../api/ErrorBoundary";


const DynamicForm = ({ 
    schema, 
    formData, 
    setFormData, 
    errorMessage, 
    setErrorMessage, 
    handleInputChange, 
    handleSubmit, 
    submitting, 
    response 
}) => {
    
    console.log("schema:", schema)
    // Handle float input with live validation (allows negative numbers)
    const validateNumericInput = (value) => {
        return /^[0-9]*\.?[0-9]*$/.test(value) ? value : ""; // Only allow numbers & decimals
      };

    
      
    const handleChange = (name, value) => {
    setFormData((prev) => {
        let newValue = value;
    
        // Find the field definition
        const field = schema.fields.find((field) => field.name === name);
    
        if (!field) return prev; // Avoid errors if field is undefined
    
        // Handle different field types
        if (field.type === "pct") {
        newValue = value / 100; // Store percentages as decimals
        } else if (field.type === "dollar") {
        newValue = value; // No transformation needed
        } else if (field.type === "list") {
        newValue = value
            .split(",") // Split by commas
            .map((item) => validateNumericInput(item.trim())) // Validate each item
            .filter((item) => item !== ""); // Remove invalid entries
        }
    
        // Additional validation (for individual number fields)
        if (field.format === "float" && isNaN(parseFloat(value))) {
        newValue = ""; // Clear invalid input
        }
    
        return { ...prev, [name]: newValue };
    });
    };

    return (
        <ErrorBoundary>
            <div className="inputs">

                <h3 className="inputs__title">{schema?.title}</h3>
                <p className="inputs__description">{schema?.description}</p>

                {schema?.fields?.map((field) => (
                    <div key={field.name} className="inputs__field_container">
                        <div className="inputs__input_title">{field.label || field.name}</div>
                        <div className="inputs__input_title">{field.type || field.name}</div>
                        {/* <div>{field.type}</div> */}
                        {field.type === "pct" ? (
                            <InputGroup inside style={{ width: 200 }}>
                                <Input
                                    placeholder={field.name}
                                    value={formData[field.name] !== undefined ? formData[field.name] * 100 : ""}
                                    onChange={(value) => handleChange(field.name, value)}
                                />
                                <InputGroup.Addon>%</InputGroup.Addon>
                            </InputGroup>
                        ) :  field.type === "dollar" ? (
                            <InputGroup inside style={{ width: 200 }}>
                                <InputGroup.Addon>$</InputGroup.Addon>
                                <Input
                                    placeholder={field.name}
                                    value={formData[field.name] !== undefined ? formData[field.name] : ""}
                                    onChange={(value) => handleChange(field.name, value)}
                                />
                            </InputGroup>
                        ) :  field.type === "float" ? (
                            <InputGroup inside style={{ width: 200 }}>
                                <Input
                                    placeholder="XX.XX"
                                    value={formData[field.name] || ""}
                                    onChange={(value) => handleChange(field.name, value)}
                                    />
                            </InputGroup>
                        ) : field.type === "num_pct_pair" ? (
                            <InputGroup inside style={{ width: 300 }}>
                                <Input
                                    placeholder="value:percent, value:percent"
                                    value={formData[field.name] || ""}
                                    onChange={(value) => handleChange(field.name, value)}
                                    />
                            </InputGroup>
                        ) : field.type === "ticker_symbol" ? (
                            <InputGroup inside style={{ width: 300 }}>
                                <Input
                                    placeholder={field.label}
                                    value={formData[field.name] || ""}
                                    onChange={(value) => handleChange(field.name, value)}
                                    />
                            </InputGroup>
                        ) : field.type === "date" ? (
                            <InputGroup inside style={{ width: 300 }}>
                                <DatePicker 
                                    oneTap format="yyyy-MM-dd" 
                                    style={{ width: 200 }} 
                                    value={formData[field.name] || new Date()}
                                    onChange={(value) => handleChange(field.name, value)}
                                    />
                                
                            </InputGroup>
                        ) : field.type === "array" ? (
                            <InputGroup inside style={{ width: 250 }}>
                                <Input
                                    placeholder="Comma-separated values"
                                    value={formData[field.name] || ""}
                                    onClick={() => setErrorMessage(null)}
                                    onChange={(value) => handleChange(field.name, value)}
                                    />
                            </InputGroup>
                        ) : (
                            <InputGroup inside style={{ width: 200 }}>
                                <Input
                                    placeholder="Enter value"
                                    value={formData[field.name] || ""}
                                    onChange={(value) => handleChange(field.name, value)}
                                    />
                            </InputGroup>
                        )}
                    </div>
                ))}

                {/* Submit and Clear Buttons */}
                <div className="inputs__button_container">
                    {schema.fields?.length > 0 && (
                    <div>
                    <Button
                        appearance="primary"
                        onClick={handleSubmit}
                        style={{ marginTop: "10px" }}
                        disabled={submitting}
                        >
                        {submitting ? "Submitting..." : "Submit"}
                    </Button>
                    <Button
                        appearance="default"
                        onClick={() => setFormData({})}
                        style={{ marginTop: "10px", marginLeft: "10px" }}
                        disabled={submitting}
                        >
                        Clear Form
                    </Button>
                    </div>
                    )}
                </div>
                <div className="inputs__response">
                    {/* Response & Error Message */}
                    {response && <p className="inputs__message">Response: {JSON.stringify(response.result)}</p>}
                    {errorMessage && <p className="inputs__error">Error: {errorMessage}</p>}
                    </div>
                </div>
        </ErrorBoundary>
    );
};

export default DynamicForm;
