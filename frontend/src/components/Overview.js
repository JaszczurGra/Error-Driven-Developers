import { Box, Paper, Typography } from '@mui/material';
import React from 'react';

const Overview = () => {
    const squares = [
        { id: 1, description: 'Square 1', number: 1 },
        { id: 2, description: 'Square 2', number: 2 },
        { id: 3, description: 'Square 3', number: 3 },
        { id: 4, description: 'Square 4', number: 4 },
    ];

    return (
        <Box className="overview-container" sx={{display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 2, flexGrow: 1, alignItems:"center", justifyContent: "center"}}>
            {squares.map(square => (
                <Paper key={square.id} sx={{height: "200px", aspectRatio: '1 / 1', backgroundColor: "rgba(159, 201, 226, 0.2)", display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', justifySelf: 'center' }}>
                    <Typography variant="h4">XX</Typography>
                    <Typography variant="caption">caption</Typography>
                </Paper>
            ))}
        </Box>
    );
};

export default Overview;