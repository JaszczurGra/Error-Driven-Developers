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
                    backgroundColor: "rgb(0, 114, 180)",
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
                    backgroundColor: "rgb(167, 33, 0)",
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