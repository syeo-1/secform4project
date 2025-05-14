import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { Box } from '@mui/material';
import { Transaction } from './types';
import StackBars from './StackBars'
import { useState } from 'react';
// import { Box } from '@mui/material';

const series = [{ data: [-2, -9, 12, 11, 6, -4] }];

// function set_timeframe_and_filing_data(event_data, transaction_data, timeframe, set_timeframe, set_filing_data) {

// }

export default function ColorScale({transaction_data}: {transaction_data: Transaction[]}) {
//   const [colorX] = React.useState<
//     'None' | 'piecewise' | 'continuous' | 'ordinal'
//   >('piecewise');
//   const [colorY, setColorY] = React.useState<'None' | 'piecewise' | 'continuous'>(
//     'None',
//   );
  const [timeframe, set_timeframe] = useState("week")
  // const [filing_data, set_filing_data] = useState(new Map())
    

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
            value={timeframe}
            onChange={(event) =>
                // set_timeframe_and_filing_data(
                //   event.target.value,
                //   transaction_data,
                //   timeframe,
                //   set_timeframe,
                //   set_filing_data
                // )
                // setColorY(event.target.value as 'None' | 'piecewise' | 'continuous')
                set_timeframe(event.target.value as 'week' | 'month' | 'year')
            }
            >
            <MenuItem value="week">Week</MenuItem>
            <MenuItem value="month">Month</MenuItem>
            <MenuItem value="year">Year</MenuItem>
            </TextField>
        </Stack>
            <StackBars filing_data={filing_data} timeframe={timeframe}>

            </StackBars>
        </Stack>
    </Box>
  );
}
