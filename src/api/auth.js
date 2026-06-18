import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export const login = async (username, password) => {
    try {
        const response = await api.post('/token', {
            grant_type: 'password',
            username,
            password,
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response.data.detail);
    }
};

export const getCurrentUser = async (token) => {
    try {
        const response = await api.get('/users/me', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response.data.detail);
    }
};