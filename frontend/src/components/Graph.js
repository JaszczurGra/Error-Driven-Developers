import { LineChart } from '@mui/x-charts/LineChart';
import { useEffect, useState } from 'react';

function Graph({ series, dataset }) {
    return (
        <div>
            <LineChart
                xAxis = {[
                    {
                        id: 'Time',
                        dataKey: 'Time',
                        scaleType: 'band',
                        valueFormatter: (date) => {
                        const d = new Date(date);
                        const year = d.getFullYear();
                        const month = String(d.getMonth() + 1).padStart(2, '0');
                        const day = String(d.getDate()).padStart(2, '0');
                        const hours = String(d.getHours()).padStart(2, '0');
                        const minutes = String(d.getMinutes()).padStart(2, '0');
                        // return `${year}-${month}-${day} ${hours}:${minutes}`;
                        return `${hours}:${minutes}`;
                        },
                    },
                ]}
                series={series}
                width={900}
                height={300}
                options={{
                    radius: 0,
                }}
                dataset={dataset}
                slotProps={{
                    legend: {
                      direction: "column",
                      position: {
                        vertical: 'middle',
                        horizontal: 'right',
                      },
                      itemMarkWidth: 20,
                      itemMarkHeight: 2,
                      markGap: 5,
                      itemGap: 10,
                    }
                  }}
                  skipAnimation={true}
                margin={{ bottom: 25, top: 20, right: 180 }}
            />
        </div>
    );
}

export default Graph;