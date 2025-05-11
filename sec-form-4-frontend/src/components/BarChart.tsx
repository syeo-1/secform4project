import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { Box } from '@mui/material';
import { Transaction } from './types';
// import { Box } from '@mui/material';

const series = [{ data: [-2, -9, 12, 11, 6, -4] }];

export default function ColorScale({transaction_data}: {transaction_data: Transaction[]}) {
  const [colorX] = React.useState<
    'None' | 'piecewise' | 'continuous' | 'ordinal'
  >('piecewise');
  const [colorY, setColorY] = React.useState<'None' | 'piecewise' | 'continuous'>(
    'None',
  );

  const filing_data = new Map()

  // same filing can have both purchases and sells, so need to distinguish them somehow when displaying data on the graph
  transaction_data.forEach((transaction_element) => {
    if (filing_data.has(transaction_element.original_form_4_text_url + " " + transaction_element.transaction_code)) {
        // increment the total value of the filing transaction

        const current_filing_value = filing_data.get(transaction_element.original_form_4_text_url + " " + transaction_element.transaction_code).total_filing_value

        if (transaction_element.transaction_code === "P") {
            // it's a purchase, so add to the total
            filing_data.set(transaction_element.original_form_4_text_url + " " + transaction_element.transaction_code, {
                acceptance_time: transaction_element.acceptance_time,
                total_filing_value: current_filing_value + (transaction_element.transaction_share_price * transaction_element.num_transaction_shares)
            })
        } else {
            // it's a sale, subtract from the total
            filing_data.set(transaction_element.original_form_4_text_url + " " + transaction_element.transaction_code, {
                acceptance_time: transaction_element.acceptance_time,
                total_filing_value: current_filing_value - (transaction_element.transaction_share_price * transaction_element.num_transaction_shares)
            })
        }

    } else {
        // create a new entry
        if (transaction_element.transaction_code === "P") {
            // purchase
            filing_data.set(transaction_element.original_form_4_text_url + " " + transaction_element.transaction_code, {
                acceptance_time: transaction_element.acceptance_time,
                total_filing_value: transaction_element.transaction_share_price * transaction_element.num_transaction_shares
            })
        } else {
            // sale
            filing_data.set(transaction_element.original_form_4_text_url + " " + transaction_element.transaction_code, {
                acceptance_time: transaction_element.acceptance_time,
                total_filing_value: -transaction_element.transaction_share_price * transaction_element.num_transaction_shares
            })
        }
    }
  })

  // now, for each of the filing_data items, use its acceptance time and total_filing value
  console.log(filing_data)



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
