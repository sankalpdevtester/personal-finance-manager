import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ProfilePage = () => {
    const [user, setUser] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axios.get('/api/profile');
                setUser(response.data);
            } catch (error) {
                console.error(error);
            }
        };
        fetchUser();
    }, []);

    const handleUpdateProfile = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.put('/api/profile', user);
            navigate('/profile');
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <Grid container spacing={2}>
            <Grid item xs={12}>
                <Paper elevation={3}>
                    <Typography variant="h4">Profile</Typography>
                    <form onSubmit={handleUpdateProfile}>
                        <label>
                            Username:
                            <input type="text" value={user.username} onChange={(event) => setUser({ ...user, username: event.target.value })} />
                        </label>
                        <br />
                        <label>
                            Email:
                            <input type="email" value={user.email} onChange={(event) => setUser({ ...user, email: event.target.value })} />
                        </label>
                        <br />
                        <Button type="submit" variant="contained">Update Profile</Button>
                    </form>
                </Paper>
            </Grid>
        </Grid>
    );
};

export default ProfilePage;