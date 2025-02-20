import { useState } from "react";
import SelectFunction from "./SelectFunction";
import MethodBox from "./MethodBox";

const Dashboard = () => {
    const [selectedMethod, setSelectedMethod] = useState(null);

    return (
      <div>
        <SelectFunction onSelect={setSelectedMethod} />
      </div>
    );
};

export default Dashboard;
