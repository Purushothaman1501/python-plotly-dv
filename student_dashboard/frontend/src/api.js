import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export const fetchDashboardData = async (filters = {}) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/dashboard`, filters);
        return response.data;
    } catch (error) {
        console.error("Error fetching dashboard data:", error);
        throw error;
    }
};
