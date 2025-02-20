import React, { useState, useEffect } from "react";
import { Dropdown } from "rsuite";
import axios from "axios";
import "../../styles/components/SelectFunction.scss"
import "@/styles/rsmod.scss"
import "@/styles/components/Dropdown.scss"

const minWidth = 120;

const SelectFunction = ({ onSelect }) => {
    const [menuData, setMenuData] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/functions/listof`);
                console.log("Data Received:", response.data);
                setMenuData(response.data);
            } catch (err) {
                setError("Failed to fetch data.");
                setMenuData([]);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    // Recursive function to render nested dropdown items
    const renderMenuItems = (items = []) => {
        return items.map((item) => {
            if (item.children && item.children.length > 0) {
                return (
                    <Dropdown.Menu key={item.id} title={item.title} style={{ minWidth }}>
                        {renderMenuItems(item.children)}
                    </Dropdown.Menu>
                );
            } else {
                return (
                    <Dropdown.Item key={item.method} onClick={() => onSelect(item.method)}>
                        {item.title}
                    </Dropdown.Item>
                );
            }
        });
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="dropdown">
            <Dropdown title="Select Function" menuStyle={{ minWidth }}>
                {renderMenuItems(menuData)}
            </Dropdown>
        </div>
    );
};

export default SelectFunction;
