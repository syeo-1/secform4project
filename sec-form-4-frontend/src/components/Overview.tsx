// give info about bigges gainers/losers of the day
// plus also info about notable insiders worth tracking
// eg. Elon, Bezos, Zucc, Buffet, Jensen (nvidia) etc...
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import OverviewCardInfo from './OverviewCardnfo';
import { useEffect, useState } from 'react'
import { Transaction } from './types';

const BASE_URL = 'http://127.0.0.1:8000/api/'

// interface Transaction {
//     reporting_owner_name: string;
//     issuer_name: string;
//     ticker_symbol: string;
//     acceptance_time: string;
//     total_filing_transaction_value: number;
//     original_form_4_text_url: string;
// }

async function retrieve_data() {
    // TODO: modify this function to get the proper data using function parameters
    // const ticker = "DUOL"
    try {
      const response = await fetch(`${BASE_URL}common/top_sale_filings`)
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const data = await response.json()
    //   console.log(`the value of the data is ${data}`)
      return data as Transaction[]
    } catch(error) {
      console.log("testing")
    }
}

export default function Overview() {

    // get the 10 largest purchases
    const [top_sale_data, set_top_sale_data] = useState<Transaction[]>([])
    const [top_purchase_data, set_top_purchase_data] = useState<Transaction[]>([])

    useEffect(() => {
        const fetchData = async () => {
            const result = await retrieve_data();
            if (result) {
                set_top_sale_data(result)
            }
        };

        fetchData();
    }, []);

    return (
        <>
            <Grid container>
                <Grid size={{ xs: 12, md: 4 }}>
                    <OverviewCardInfo data_list={top_sale_data} title="Top Sale Data"/>
                </Grid>
                <Grid size={{ xs: 12, md: 4}}>
                    <OverviewCardInfo data_list={top_sale_data} title="Top Purchase Data"/>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                    <OverviewCardInfo data_list={top_sale_data} title="Notable Names"/>
                </Grid>
            </Grid>
        </>
    )
}