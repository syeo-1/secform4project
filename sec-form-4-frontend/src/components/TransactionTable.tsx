import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { Transaction } from './types';

function createData(transaction_element: Transaction) {
  const transaction_code = transaction_element.transaction_code
  const acceptance_time = transaction_element.acceptance_time
  const issuer_name = transaction_element.issuer_name
  const ticker_symbol = transaction_element.ticker_symbol
  const reporting_owner_name = transaction_element.reporting_owner_name
  const num_transaction_shares = transaction_element.num_transaction_shares
  const transaction_share_price = transaction_element.transaction_share_price
  const form_4_id = transaction_element.form_4_id
  return {
    transaction_code,
    acceptance_time,
    issuer_name,
    ticker_symbol,
    reporting_owner_name,
    num_transaction_shares,
    transaction_share_price,
    form_4_id
  }
}

// const rows = [
//   createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
//   createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
//   createData('Eclair', 262, 16.0, 24, 6.0),
//   createData('Cupcake', 305, 3.7, 67, 4.3),
//   createData('Gingerbread', 356, 16.0, 49, 3.9),
// ];

export default function DenseTable({transaction_data}: {transaction_data: Transaction[]}) {

  // console.log(`here, transaction data is now: ${JSON.stringify(transaction_data)}`)

  const formatted_transaction_data: any = []

  for (const transaction_element of transaction_data) {
    formatted_transaction_data.push(createData(transaction_element))
  }
  
  // console.log(`data is now: ${JSON.stringify(formatted_transaction_data)}`)

  // I'll need to fetch the data for the rows via the api
  // after fetching, store the rows in the array

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>Transaction Type</TableCell>
            <TableCell>Acceptance Time</TableCell>
            <TableCell align="right">Company Name</TableCell>
            <TableCell align="right">Symbol</TableCell>
            <TableCell align="right">Reporting Owner</TableCell>
            <TableCell align="right">Shares Traded</TableCell>
            <TableCell align="right">Transaction Share Price (USD)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {formatted_transaction_data.map((row: any) => {
            // console.log("form 4 id: ", row.form_4_id)
            return (<TableRow
              key={row.form_4_id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.transaction_code}
              </TableCell>
              <TableCell align="right">{row.acceptance_time}</TableCell>
              <TableCell align="right">{row.issuer_name}</TableCell>
              <TableCell align="right">{row.ticker_symbol}</TableCell>
              <TableCell align="right">{row.reporting_owner_name}</TableCell>
              <TableCell align="right">{row.num_transaction_shares}</TableCell>
              <TableCell align="right">{`$${row.transaction_share_price}`}</TableCell>
            </TableRow>
            )})}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
