import { useState } from "react";
import SelectFunction from "./SelectFunction";
import MethodBox from "./MethodBox";
import "@/styles/components/MethodBox.scss"

const MethodSelector = () => {
    const [selectedMethod, setSelectedMethod] = useState(null);

    return (
        <div className="methodbox">
            <h3 className="text-2xl font-bold mb-4">Select a Function</h3>
            
            {/* Function Selector */}
            <SelectFunction onSelect={setSelectedMethod} />

            {/* Display MethodBox when a method is selected */}
            {selectedMethod && (
                <div className="methodbox__container">
                    <MethodBox method={selectedMethod} />
                </div>
            )}
        </div>
    );
};

export default MethodSelector;
