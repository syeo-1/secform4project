import * as React from 'react';
import { BarChart, BarChartProps } from '@mui/x-charts/BarChart';
import { addLabels, balanceSheet } from './AddLabelStack';

export default function StackBars({filing_data}: {filing_data: Map<any, any>}) {
  return (
    <BarChart
      dataset={balanceSheet}
      series={addLabels([
        { dataKey: 'total_purchase_value', stack: 'net_transaction_value', color: '#089981' },
        { dataKey: 'total_sale_value', stack: 'net_transaction_value', color: '#f23645'},
      ])}
      xAxis={[{
        scaleType: 'band',
        dataKey: 'datetime'

     }]}
    //   yAxis={[{ width: 80 }]}
    slotProps={{
        legend: { hidden: true }
    }}
    // margin={{left: 4000}}
    // height={350}
      {...config}
    />
  );
}

const config: Partial<BarChartProps> = {
  height: 350,
  margin: { left: 100 },
//   hideLegend: true,
};