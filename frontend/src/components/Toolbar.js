import { Box } from "@mui/material";
import { Button } from "@mui/material";

function Toolbar({isSimulating, swapIsSimulation, resetSimulation}) {
    return (
        <Box sx={{ 
            position: 'fixed', 
            bottom: 0, 
            left: '50%', 
            transform: 'translateX(-50%)', 
            display: 'flex', 
            padding: 0, 
            alignItems: 'center', 
            gap: 3,
            padding: '10px'
        }}>
            <Button 
                variant="contained" 
                sx={{ 
                    backgroundColor: "rgb(48, 161, 226)",
                    borderRadius: '50%', 
                    width: '70px', 
                    height: '70px' 
                }}
                onClick={swapIsSimulation}
            >
                {isSimulating ? 'Pause' : 'Resume'}
            </Button>
            <Button 
                variant="contained" 
                sx={{ 
                    backgroundColor: "white", 
                    color: "rgb(219, 56, 15)", 
                    borderRadius: '50%', 
                    width: '70px', 
                    height: '70px' 
                }}
                onClick={resetSimulation}
            >
                Reset
            </Button>
        </Box>
    );
}

export default Toolbar;