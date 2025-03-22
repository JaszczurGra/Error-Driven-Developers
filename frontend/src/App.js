import logo from './logo.svg';
import './App.css';
import Graph from './components/Graph';
import Toolbar from './components/Toolbar';
import { Box } from '@mui/material';
import Overview from './components/Overview';
import Grid from './components/Grid';
import simulation_data from "./const/simulation_data.json";
import actions_data from "./const/actions_data.json";
import { use, useEffect, useState } from 'react';

function App() {
  const [dataset, setDataset] = useState([]);
  const [actions, setActions] = useState([]);
  const [isSimulating, setIsSimulating] = useState(true);

  useEffect(() => {
    let interval;
    if (isSimulating) {
      interval = setInterval(() => {
        setDataset(prevData => {
          const newIndex = prevData.length + 1;
          if (newIndex >= simulation_data.length) {
            return prevData;
          }
          const newData = simulation_data[newIndex];
          const newActions = actions_data.filter(action => action.time === newData.Time);
          if (newActions.length > 0) {
            setActions(prevActions => [...newActions, ...prevActions]);
          }
          return [
            ...prevData,
            newData
          ];
        });
      }, 1000);
    }

    return () => clearInterval(interval);
  }, [isSimulating, simulation_data]);


  const startSimulation = () => setIsSimulating(true);
  const stopSimulation = () => setIsSimulating(false);
  const resetSimulation = () => {
    setIsSimulating(true);
    setDataset([]);
  };

  return (
    <div className="App">
      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2}}>
        <Box sx={{ display: 'grid',}}>
        <Graph 
            series = {[
              {
                id: 'Token Balance',
                label: 'Token Balance',
                dataKey: 'Token Balance',
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
                dataKey: 'Purchase Price',
                showMark: false,
              },
              {
                id: 'P2P Price',
                label: 'P2P Price',
                dataKey: 'P2P Price',
                showMark: false,
              },
              {
                id: 'Grid Price',
                label: 'Grid Price',
                dataKey: 'Grid Price',
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
                dataKey: 'Total Consumption',
                showMark: false,
              },
              {
                id: 'Total Production',
                label: 'Total Production',
                dataKey: 'Total Production',
                showMark: false,
              },
            ]}
            dataset = {dataset}
        />
      </Box>
        <Box>
          <Overview/>
          <Grid data={actions}/>
        </Box>
      </Box>
      <Toolbar startSimulation={startSimulation} stopSimulation={stopSimulation} resetSimulation={resetSimulation}/>
    </div>
  );
}

export default App;
