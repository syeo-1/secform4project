import React from 'react';
import Plot from 'react-plotly.js';

const BarChartBig = () => {
  const numPoints = 10000;
  const x = Array.from({ length: numPoints }, (_, i) => `Item ${i + 1}`);
  const y = Array.from({ length: numPoints }, () => Math.floor(Math.random() * 1000));

  return (
    <div style={{ width: '100%', height: '600px', overflowX: 'scroll' }}>
      <Plot
        data={[
          {
            type: 'bar',
            x: x,
            y: y,
            marker: { color: 'dodgerblue' },
          },
        ]}
        layout={{
          title: '10,000-Bar Chart',
          xaxis: { title: 'Items', showticklabels: false },
          yaxis: { title: 'Value' },
          margin: { t: 50 },
          bargap: 0.1,
        }}
        config={{ responsive: true }}
        useResizeHandler
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
};

export default BarChartBig;
