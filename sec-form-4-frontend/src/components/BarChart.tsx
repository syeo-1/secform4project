import * as React from 'react';
// import { BarChart } from '@mui/x-charts/BarChart';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { Select } from '@mui/material';
import { Box } from '@mui/material';
import { Transaction } from './types';
import StackBars from './StackBars'
import { useRef, useEffect, useState } from 'react';
import '../index.css'
import BarChartBig from './BarChartBig';
// import { Box } from '@mui/material';

const series = [{ data: [-2, -9, 12, 11, 6, -4] }];

// function set_timeframe_and_filing_data(event_data, transaction_data, timeframe, set_timeframe, set_filing_data) {

// }

// function for useeffect, so whenever the timeframe changes, set_transaction is run
// the set transaction takes the given unprocessed transaction_data and filters out all
// elements not within the given timeframe using the acceptance time attribute

function timeframe_filter_transaction_data(transaction_data: Transaction[], timeframe: string) {
  // takes transaction_data and timeframe, and based on that filters out elements
  // not within the given timeframe based on acceptance time attribute
  const filtered_transaction_data = new Array<Transaction>();

  const now = new Date();
  const oldest_allowable_date = new Date();
  if (timeframe === 'week') {
    oldest_allowable_date.setDate(now.getDate() - 7);
  } else if (timeframe === 'month') {
    oldest_allowable_date.setDate(now.getDate() - 30)
  } else if (timeframe === 'six-months') {
    oldest_allowable_date.setDate(now.getDate() - 180)
  } else if (timeframe === 'year') {
    oldest_allowable_date.setDate(now.getDate() - 365)
  }

  transaction_data.forEach((transaction_element) => {
    const transaction_element_acceptance_time_iso = new Date(transaction_element.acceptance_time)
    // console.log(`the acceptance time in iso format: ${transaction_element_acceptance_time_iso}`)
    // console.log(`oldest allowable date is: ${oldest_allowable_date}`)
    

    if (transaction_element_acceptance_time_iso >= oldest_allowable_date) {
      filtered_transaction_data.push(transaction_element)
    }
  })


  return filtered_transaction_data
}

export default function BarChart({transaction_data, set_transactions, transaction_data_copy}: {transaction_data: Transaction[], set_transactions: React.Dispatch<React.SetStateAction<Transaction[]>>, transaction_data_copy: Transaction[]}) {
  const [timeframe, set_timeframe] = useState("month")
  const has_run = useRef(false)

  const filing_data = new Map()

  // const transaction_data_clone = structuredClone(transaction_data)

  useEffect(() => {
    const filtered_transaction_data = timeframe_filter_transaction_data(transaction_data_copy, timeframe)
    set_transactions(filtered_transaction_data)
  }, [transaction_data_copy])

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


  return (
    <Box sx={{ display: 'flex', flexDirection: 'inherit', justifyContent: 'center', width: '100%'}}>
        <Stack direction="column" spacing={1} sx={{ width: '100%', maxWidth: '95%', margin: '0 auto', marginTop: 2}}>
        <Stack direction="row" spacing={1}>
            <Select
            // placeholder='Timeframe'
            // sx={{ minWidth: 150, backgroundColor: 'black',
            //   // label: {color: 'blue'},
            //   '& .MuiInputBase-input': {
            //     color: 'white', // or any other color
            //   },
            //   },
            sx={{
                backgroundColor: 'black',
                color: 'white',
                '& .MuiSvgIcon-root': {
                  color: 'white',
                },
              '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'dodgerblue', 
                  borderRadius: '5px',
                  // borderWidth: '2px',
                },
                '&:hover .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'dodgerblue',
                  borderRadius: '5px',
                },
                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'dodgerblue',
                  borderRadius: '3px',
                  borderWidth: '2px'
                },
              }}
            MenuProps={{
              PaperProps: {
                sx: {
                  backgroundColor: 'black',
                  color: 'white',
                  // padding: 0,
                  // borderRadius: 0,
                },
              },
              MenuListProps: {
                sx: {
                  // padding: 0,
                  // margin: 0,
                },
              },
            }}
            // color='error'
            label=""
            value={timeframe}
            onChange={(event) => {
              set_timeframe(event.target.value as 'week' | 'month' | 'six months' | 'year')
              // console.log(event.target.value)
              // console.log(transaction_data_copy)
              const filtered_transaction_data = timeframe_filter_transaction_data(transaction_data_copy, event.target.value)
              set_transactions(filtered_transaction_data)
            }}
            >
            <MenuItem className="menu-item" value="week">Week</MenuItem>
            <MenuItem className="menu-item" value="month">Month</MenuItem>
            <MenuItem className="menu-item" value="six-months">6 Months</MenuItem>
            <MenuItem className="menu-item" value="year">Year</MenuItem>
            </Select>
        </Stack>
            <StackBars filing_data={filing_data} timeframe={timeframe}>

            </StackBars>
            {/* <BarChartBig></BarChartBig> */}

        </Stack>
    </Box>
  );
}
