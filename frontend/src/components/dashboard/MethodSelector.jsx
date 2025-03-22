import { useState } from "react";
import SelectFunction from "./SelectFunction";
import MethodBox from "./MethodBox";
import "@/styles/components/MethodBox.scss";

const MethodSelector = () => {
    const [selectedMethods, setSelectedMethods] = useState([]); // Store multiple methods

    const handleSelect = (method) => {
        setSelectedMethods((prevMethods) => {
            // Prevent duplicates
         
                return [method, ...prevMethods];
           
        });
    };

    const handleClose = (methodToRemove) => {
        setSelectedMethods((prevMethods) =>
            prevMethods.filter((method) => method !== methodToRemove)
        );
    };

    return (
        <div className="methodbox">
            <h3 className="text-2xl font-bold mb-4">Select a Function</h3>
            
            {/* Function Selector */}
            <SelectFunction onSelect={handleSelect} />

            {/* Render a MethodBox for each selected method */}
            <div className="methodbox__container">
                {selectedMethods.map((method, index) => (
                    <MethodBox 
                        key={index} 
                        method={method}
                        onClose={handleClose} // ✅ Pass onClose function 
                    />
                ))}
            </div>
        </div>
    );
};

export default MethodSelector;
