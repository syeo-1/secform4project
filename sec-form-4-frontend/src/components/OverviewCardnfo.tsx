// info for the columns in the home page

// import { useEffect, useState } from "react";
import { Transaction } from './types';
import BasicMenu from './BasicMenu';
import { useEffect, useState } from 'react'

// interface OverviewPropData {
//     // fetch_data: () => Promise<(string | any[])[]>;
//     // data_list: (string | any[])[] | Promise<(string | any[])[]>;
//     data_list: Transaction[] | string[]
// }
const BASE_API_URL = 'http://127.0.0.1:8000/api/'
const BASE_FRONTEND_URL = 'http://localhost:5173/'

async function retrieve_data(time_interval: string, transaction_type: string) {
    // TODO: modify this function to get the proper data using function parameters
    // const ticker = "DUOL"
    try {
      const response = await fetch(`${BASE_API_URL}common/top_filings/?time_interval=${time_interval}&transaction_type=${transaction_type}`)
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

export default function OverviewCardInfo({className, title, transaction_type}: { className: string, title: string, transaction_type: string}) {



    // get the 10 largest purchases
    const [top_transaction_data, set_top_transaction_data] = useState<Transaction[]>([])
    const [time_interval, set_time_interval] = useState("Day")
    // const [person_or_company, set_person_or_company] = useState("Person")
    
    const handle_time_interval = (interval: string) => {
        set_time_interval(interval)
        // console.log(time_interval)
    }

    // const handle_person_or_company = (value: string) => {
    //     // console.log("PERSON")
    //     // console.log(value)
    //     set_person_or_company(value)
    // }

    useEffect(() => {
        const fetchData = async () => {
            const result = await retrieve_data(time_interval, transaction_type);
            if (result) {
                set_top_transaction_data(result)
            }
        };

        fetchData();
    }, [time_interval]);

    const data_list_li = top_transaction_data.map((data_item: Transaction, index: number) => <li className={className} key={index}><><a href={`${BASE_FRONTEND_URL}info/${data_item.reporting_owner_name.replace(/ /g, "%20")}`}>{data_item.reporting_owner_name}</a></></li>);

    return (
        <div className={className}>
            <h2>{title}</h2>
            <BasicMenu options={['Day','Week', 'Month', 'Year']} initial_title='Day' on_menu_change={handle_time_interval}/>
            {/* <BasicMenu options={['Person', 'Company']} initial_title='Person' on_menu_change={handle_person_or_company}/> */}
            <ol>
                {data_list_li}
            </ol>
        </div>
    )
}