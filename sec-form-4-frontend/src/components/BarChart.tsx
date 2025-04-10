import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { Box } from '@mui/material';
// import { Box } from '@mui/material';

const series = [{ data: [-2, -9, 12, 11, 6, -4] }];

export default function ColorScale() {
  const [colorX] = React.useState<
    'None' | 'piecewise' | 'continuous' | 'ordinal'
  >('piecewise');
  const [colorY, setColorY] = React.useState<'None' | 'piecewise' | 'continuous'>(
    'None',
  );

  return (
    <Box sx={{ display: 'flex', flexDirection: 'inherit', justifyContent: 'center', width: '100%'}}>
        <Stack direction="column" spacing={1} sx={{ width: '100%', maxWidth: 600, margin: '0 auto', marginTop: 2}}>
        <Stack direction="row" spacing={1}>
            <TextField
            select
            sx={{ minWidth: 150 }}
            label="Timeframe"
            value={colorY}
            onChange={(event) =>
                setColorY(event.target.value as 'None' | 'piecewise' | 'continuous')
            }
            >
            <MenuItem value="None">Today</MenuItem>
            <MenuItem value="piecewise">Week</MenuItem>
            <MenuItem value="continuous">Month</MenuItem>
            </TextField>
        </Stack>

        <BarChart
            height={300}
            sx={{
                flexDirection: 'inherit'
            }}
            width={500}
            grid={{ horizontal: true }}
            series={series}
            margin={{
            top: 10,
            bottom: 20,
            }}
            yAxis={[
            {
                colorMap:
                (colorY === 'continuous' && {
                    type: 'continuous',
                    min: -10,
                    max: 10,
                    color: ['red', 'green'],
                }) ||
                (colorY === 'piecewise' && {
                    type: 'piecewise',
                    thresholds: [0],
                    colors: ['red', 'green'],
                }) ||
                undefined,
            },
            ]}
            xAxis={[
            {
                scaleType: 'band',
                data: [
                new Date(2019, 1, 1),
                new Date(2020, 1, 1),
                new Date(2021, 1, 1),
                new Date(2022, 1, 1),
                new Date(2023, 1, 1),
                new Date(2024, 1, 1),
                ],
                valueFormatter: (value) => value.getFullYear().toString(),
                colorMap:
                (colorX === 'ordinal' && {
                    type: 'ordinal',
                    colors: [
                    '#ccebc5',
                    '#a8ddb5',
                    '#7bccc4',
                    '#4eb3d3',
                    '#2b8cbe',
                    '#08589e',
                    ],
                }) ||
                (colorX === 'continuous' && {
                    type: 'continuous',
                    min: new Date(2019, 1, 1),
                    max: new Date(2024, 1, 1),
                    color: ['green', 'orange'],
                }) ||
                (colorX === 'piecewise' && {
                    type: 'piecewise',
                    thresholds: [new Date(2021, 1, 1), new Date(2023, 1, 1)],
                    colors: ['blue', 'red', 'blue'],
                }) ||
                undefined,
            },
            ]}
        />
        </Stack>
    </Box>
  );
}
