import React from "react";
import MethodSelector from "./components/dashboard/MethodSelector";


const App = () => {
    return (
        <div className="app">
            <div className="app__container">
                <h3 className="app__title">Function Processor</h3>
                <MethodSelector />
            </div>
        <div>
            {/* <FormTest /> */}
        </div>
        </div>
    );
};

export default App;
