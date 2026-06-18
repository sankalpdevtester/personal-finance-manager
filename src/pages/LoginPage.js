import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await login(username, password);
            navigate('/dashboard');
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <Box sx={{ width: '100%', height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    sx={{ width: '100%', marginBottom: 2 }}
                />
                <TextField
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    sx={{ width: '100%', marginBottom: 2 }}
                />
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <Button type="submit" variant="contained" sx={{ width: '100%' }}>
                    Login
                </Button>
            </form>
        </Box>
    );
};

export default LoginPage;