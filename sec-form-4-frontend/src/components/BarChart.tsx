import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { Box } from '@mui/material';
import { Transaction } from './types';
import StackBars from './StackBars'
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
//   console.log(filing_data)



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
            <StackBars filing_data={filing_data} timeframe={'week'}>

            </StackBars>
        </Stack>
    </Box>
  );
}
