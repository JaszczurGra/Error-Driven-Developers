import logo from './logo.svg';
import './App.css';
import Graph from './components/Graph';
import Toolbar from './components/Toolbar';
import { Box } from '@mui/material';
import Overview from './components/Overview';
import Grid from './components/Grid';
import actions_data from "./const/actions_data.json";
import { useEffect, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  const [dataset, setDataset] = useState([]);
  const [actions, setActions] = useState([]);
  const [simulationData, setSimulationData] = useState([]);
  const [isSimulating, setIsSimulating] = useState(true);

  useEffect(() => {
    async function fetchSimulationData() {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/simulation`);
        const data = await response.json();
        setSimulationData(data);
      } catch (error) {
        console.error("Error fetching simulation data:", error);
      }
    }

    fetchSimulationData();
  }, []);

  useEffect(() => {
    let interval;
    if (isSimulating && simulationData) {
      interval = setInterval(() => {
        setDataset(prevData => {
          const newIndex = prevData.length + 1;
          if (newIndex >= simulationData.length) {
            return prevData;
          }
          const newData = simulationData[newIndex];
          const newActions = actions_data.filter(action => action.time === newData.time);
          if (newActions.length > 0) {
            setActions(prevActions => {
              const uniqueActions = newActions.filter(newAction => 
                !prevActions.some(prevAction => 
                  prevAction.time === newAction.time && prevAction.action === newAction.action
                )
              );
              return [...uniqueActions, ...prevActions];
            });
          }
          return [
            ...prevData,
            newData
          ];
        });
      }, 1000);
    }

    return () => clearInterval(interval);
  }, [isSimulating, simulationData]);

  const swapIsSimulation = () => setIsSimulating(() => !isSimulating);
  const resetSimulation = () => {
    setIsSimulating(true);
    setDataset([]);
    setActions([]);
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <div className="App">
        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr'}}>
          <Box sx={{ display: 'grid',}}>
          <Graph 
              series = {[
                {
                  id: 'Token Balance',
                  label: 'Token Balance',
                  dataKey: 'token_balance',
                  showMark: false,
                },
              ]}
              dataset = {dataset}
          />
            <Graph 
              series = {[
                {
                  id: 'Purchase Price',
                  label: 'Purchase Price',
                  dataKey: 'purchase_price',
                  showMark: false,
                },
                {
                  id: 'P2P Price',
                  label: 'P2P Price',
                  dataKey: 'p2p_price',
                  showMark: false,
                },
                {
                  id: 'Grid Price',
                  label: 'Grid Price',
                  dataKey: 'grid_price',
                  showMark: false,
                }
              ]}
              dataset = {dataset}
          />
          <Graph 
              series = {[
                {
                  id: 'Total Consumption',
                  label: 'Total Consumption',
                  dataKey: 'total_consumption',
                  showMark: false,
                },
                {
                  id: 'Total Production',
                  label: 'Total Production',
                  dataKey: 'total_production',
                  showMark: false,
                },
              ]}
              dataset = {dataset}
          />
          <Graph 
              series = {Object.keys(dataset[0] || {})
                .filter(key => key.startsWith('storage_level'))
                .map(key => ({
                  id: key.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase()),
                  label: key.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase()),
                  dataKey: key,
                  showMark: false,
                }))}
              dataset = {dataset}
          />
        </Box>
          <Box>
            {/* <Overview/> */}
            <Grid data={actions}/>
          </Box>
        </Box>
        <Toolbar isSimulating={isSimulating} swapIsSimulation={swapIsSimulation} resetSimulation={resetSimulation}/>
      </div>
    </ThemeProvider>
  );
}

export default App;
