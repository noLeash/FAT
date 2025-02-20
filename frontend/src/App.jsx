import React from "react";
import MethodSelector from "./components/dashboard/MethodSelector";

const App = () => {
    return (
        <div className="app">
            <div className="app-container">
                <h3 className="text-3xl font-bold mb-4">Function Processor</h3>
                <MethodSelector />
            </div>
        </div>
    );
};

export default App;
