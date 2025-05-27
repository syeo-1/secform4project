import React from 'react';
import Plot from 'react-plotly.js';
import { Data, Layout } from 'plotly.js'

export default function BarChartBig({processed_filing_data}: {processed_filing_data: {
  datetime: string;
  total_purchase_value: number,
  total_sale_value: number
}[]}) {
  const datetime_strings = processed_filing_data.map((filing_data) => filing_data.datetime)
  const purchase_data = processed_filing_data.map((filing_data) => filing_data.total_purchase_value)
  const sale_data = processed_filing_data.map((filing_data) => filing_data.total_sale_value)

  const purchase_data_and_times: Data = {
    x: datetime_strings,
    y: purchase_data,
    type: 'bar',
    name: 'Purchases in USD',
    marker: {
      color: '#089981'
    },
    hoverinfo: 'x+y'
  }

  const sale_data_and_times: Data = {
    x: datetime_strings,
    y: sale_data,
    type: 'bar',
    name: 'Sales in USD',
    marker: {
      color: '#f23645'
    }
  }

  const layout: Partial<Layout> = {
    barmode: 'relative',
    // width: '100%',
    height: 400,
    autosize: true,
    paper_bgcolor: 'black',
    plot_bgcolor: 'black',
    hovermode: 'closest',
    margin: {
      t: 10,
      b: 50
    },
    font: {
      color: 'white'
    },
    xaxis: {
      showgrid: true,
      gridcolor: '#282a35',
      gridwidth: 1,
    },
    yaxis: {
      showgrid: true,
      gridcolor: '#282a35',
      gridwidth: 1,
    }
  };

  return (
    <div style={{ 
      overflowX: 'auto',
      backgroundColor: 'black',
      width: '100%'
    }}>
      <Plot
        data={[purchase_data_and_times, sale_data_and_times]}
        layout={layout}
        config={{ responsive: true }}
        style={{width: '100%'}}
      />
    </div>
  );
};
