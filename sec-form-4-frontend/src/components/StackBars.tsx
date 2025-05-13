import * as React from 'react';
import { BarChart, BarChartProps } from '@mui/x-charts/BarChart';
import { addLabels, balanceSheet } from './AddLabelStack';

export default function StackBars() {
  return (
    <BarChart
      dataset={balanceSheet}
      series={addLabels([
        { dataKey: 'total_purchase_value', stack: 'net_transaction_value' },
        { dataKey: 'total_sale_value', stack: 'net_transaction_value' },
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