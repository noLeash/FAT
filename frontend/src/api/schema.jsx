import axios from "axios";

/**
 * Fetches the schema for a given method.
 * @param {string} method - The method identifier for which to fetch the schema.
 * @returns {Promise<Object|null>} - A promise that resolves to the schema object or null if an error occurs.
 */
export const fetchSchema = async (method) => {
    if (!method) {
        console.warn("fetchSchema called without a method.");
        return null;
    }

    try {
        const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/schema`, {
            params: { method }, // Send method as a query parameter
        });

        // Debugging: Log the received schema
        // console.log("Fetched schema:", response.data);

        // Ensure the response contains a valid schema
        if (!response.data || !response.data.fields) {
            console.error("Invalid schema structure received:", response.data);
            return null;
        }

        return response.data;
    } catch (error) {
        console.error("Error fetching schema:", error.response?.data || error.message);
        return null;
    }
};
