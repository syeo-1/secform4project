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
    // retrieve_data()
    // .then((data) => {
    //     console.log(`data is actually ${JSON.stringify(data, null, 2)}`)
    // })

    const [top_sale_data, set_top_sale_data] = useState<Transaction[]>([])
    const [top_purchase_data, set_top_purchase_data] = useState<Transaction[]>([])

    const data = retrieve_data()
        // .then((result) => {

        //     let top_results = new Array<Transaction>();

        //     result?.forEach((item) => {
        //         console.log(`blah blah ${JSON.stringify(item)}`)
        //         top_results.push(item)
        //     })

        //     return top_results;
        // })
    // console.log(`data value is ${JSON.stringify(data, null, 2)}`)
    // set_top_sale_data(data)
    useEffect(() => {
        const fetchData = async () => {
            const result = await retrieve_data();
            if (result) {
                set_top_sale_data(result); // ✅ correct type: Transaction[]
            }
        };

        fetchData();
    }, []);

    // console.log(top_sale_data)
    // console.log(`this is the data ${JSON.stringify(data)}`)
    // console.log(`data is actually ${JSON.stringify(stuff, null, 2)}`)
    // const data_get = purchase_data.json()
    // console.log(`purchase data value is: ${purchase_data}`)

    // get the 10 largest sells
    // const sale_data = retrieve_data()

    // just create a list of names you think are interesting (hardcoded for now) in frontend!
    // const notable_names = [
    //     "Musk Elon",
    //     "BUFFETT Warren E",
    //     "BEZOS JEFFREY P",
    //     "FROST PHILLIP MD",
    //     "Zuckerberg Mark",
    //     "BAKER BROS. ADVISORS LP",
    //     "GATES WILLIAM H III",
    //     "Perceptive Advisors LLC",
    //     "CARL C. ICAHN",
    //     "TANG CAPITAL MANAGEMENT LLC"
    // ]

    // some random names available in the database for seeing if things work!
    // const notable_names = [
    //     "Aebersold Sarah",
    //     "Agah Ramtin",
    //     "AGRAWAL HEENA",
    //     "Ahuja Amrita",
    //     "Akinsanya Karen",
    //     "Allen Charles W",
    //     "Allison Eric",
    //     "Altman Peter",
    //     "AMIN TARANG",
    //     "Anderson Joshua Joseph"
    // ]

    // console.log(notable_names)

    return (
        <>
            <Grid container>
                <Grid size={{ xs: 12, md: 4 }}>
                    <OverviewCardInfo data_list={top_sale_data}/>
                </Grid>
                <Grid size={{ xs: 12, md: 4}}>
                    <OverviewCardInfo data_list={top_sale_data}/>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                    <OverviewCardInfo data_list={top_sale_data}/>
                </Grid>
            </Grid>
        </>
    )
}