import * as React from 'react';
import { BarChart, BarChartProps } from '@mui/x-charts/BarChart';
import { addLabels, balanceSheet } from './AddLabelStack';
import BarChartBig from './BarChartBig';


function get_last_n_day_strings(n: number): string[] {
  const result: string[] = [];
  const today = new Date();

  for (let i = n - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    result.push(date.toISOString().split('T')[0]); // Format: 'YYYY-MM-DD'
  }

  return result;
}


function process_filing_data_for_barchart(filing_data: any, timeframe: string) {
  // takes the given filing data and timeframe and returns two things within an object:
  // 1. the data needed to be passed to the chart to be displayed
  // 2. the individual dates or hours needed for the x-axis in the barchart

  let timeframe_strings: string[] 
  const processed_filing_data = new Map()

  if (timeframe === 'week') {
    timeframe_strings = get_last_n_day_strings(7)
  } else if (timeframe === 'month') {
    timeframe_strings = get_last_n_day_strings(30)
  } else if (timeframe === 'six-months') {
    timeframe_strings = get_last_n_day_strings(180)
  } else if (timeframe === 'year') {
    timeframe_strings = get_last_n_day_strings(365)
  }

  // TODO: should try and figure out how to improve performance here since O(N)^2
  // maybe could just iterate through the map and do a date check instead of going through each day?
  filing_data.forEach((value: any, _: string) => {
    for (const time_string of timeframe_strings) {
      // filing_data.forEach((value: any, _: string) => {
      // modify the total purchase and sale values for that day
      if (value.acceptance_time.includes(time_string) && processed_filing_data.has(time_string)) {
        const current_purchase_value = processed_filing_data.get(time_string).total_purchase
        const current_sale_value = processed_filing_data.get(time_string).total_sale

        if (value.total_filing_value > 0) {
          processed_filing_data.set(time_string, {
            total_purchase: current_purchase_value + value.total_filing_value,
            total_sale: current_sale_value
          })
        } else {
          processed_filing_data.set(time_string, {
            total_purchase: current_purchase_value,
            total_sale: current_sale_value + value.total_filing_value
          })
        }
      } else if (value.acceptance_time.includes(time_string) && !processed_filing_data.has(time_string)) {
        // set initial value for given timeframe
        if (value.total_filing_value > 0) {
          processed_filing_data.set(time_string, {
            total_purchase: value.total_filing_value,
            total_sale: 0
          })
        } else if (value.total_filing_value < 0) {
          processed_filing_data.set(time_string, {
            total_purchase: 0,
            total_sale: value.total_filing_value
          })
        } else { // TODO: is this necessary???
          processed_filing_data.set(time_string, {
            total_purchase: 0,
            total_sale: 0
          })
        }
      } else if (!processed_filing_data.has(time_string)) {
        // need to still show no activity happening on other days
        processed_filing_data.set(time_string, {
          total_purchase: 0,
          total_sale: 0
        })
      }
    }
  })

  const processed_and_formatted_filing_data = Array.from(processed_filing_data).map(
    ([timestamp, value]) => (
      {
        datetime: timestamp,
        total_purchase_value: value.total_purchase,
        total_sale_value: value.total_sale
      })
  )

  // console.log(processed_and_formatted_filing_data)

  return processed_and_formatted_filing_data

}

export default function StackBars({filing_data, timeframe}: {filing_data: Map<any, any>, timeframe: string}) {

  // take the filing data and process so that can get the proper total purchase and sale data
  // based on the given timeframe
  const processed_filing_data = process_filing_data_for_barchart(filing_data, timeframe)

  return (
    <>
      {/* <BarChart
        sx={
          {
          '& .MuiChartsGrid-line': {
            stroke: '#26252b',
            strokeWidth: 1,
          },
        }
        }
        dataset={processed_filing_data}
        series={addLabels([
          { dataKey: 'total_purchase_value', stack: 'net_transaction_value', color: '#089981' },
          { dataKey: 'total_sale_value', stack: 'net_transaction_value', color: '#f23645'},
        ])}
        xAxis={[{
          scaleType: 'band',
          dataKey: 'datetime',
          tickLabelStyle: {fill: 'lightslategray'}
      }]}
      yAxis={[
        {
          tickLabelStyle: {fill: 'lightslategray'}
        }
      ]}
      grid={{
        horizontal: true,
        vertical: true
      }}
      //   yAxis={[{ width: 80 }]}
      slotProps={{
          legend: { hidden: true }
      }}
      margin={{left: 100}}
      height={350}
      /> */}
      <BarChartBig processed_filing_data={processed_filing_data}></BarChartBig>
    </>
  );
}
