// info for the columns in the home page

// import { useEffect, useState } from "react";
import { Transaction } from './types';
import BasicMenu from './BasicMenu';
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router';

// interface OverviewPropData {
//     // fetch_data: () => Promise<(string | any[])[]>;
//     // data_list: (string | any[])[] | Promise<(string | any[])[]>;
//     data_list: Transaction[] | string[]
// }
const BASE_API_URL = 'http://127.0.0.1:8000/api/'
const BASE_FRONTEND_URL = 'http://localhost:5173/'

async function retrieve_data(time_interval: string, transaction_type?: string) {
    // TODO: modify this function to get the proper data using function parameters
    // const ticker = "DUOL"
    try {
      let response
    
      if (transaction_type != null) {
        response = await fetch(`${BASE_API_URL}common/top_filings/?time_interval=${time_interval}&transaction_type=${transaction_type}`)
        const data = await response.json()
        //   console.log(`the value of the data is ${data}`)
        return data as Transaction[]
      } else {
        response = await fetch(`${BASE_API_URL}common/top_activity/?time_interval=${time_interval}`)
        const data = await response.json()
        return data as string[]
      }
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    } catch(error) {
      console.log("testing")
    }
}

export default function OverviewCardInfo({homepage_text_css, homepage_title_css, title, transaction_type}: { homepage_text_css: string, homepage_title_css: string, title: string, transaction_type?: string}) {



    // get the 10 largest purchases
    const [top_transaction_data, set_top_transaction_data] = useState<Transaction[] | string[]>([])
    const [top_activity_tickers, set_top_activity_tickers] = useState<Transaction[] | string[]>([])
    const [time_interval, set_time_interval] = useState("Day")
    // const [person_or_company, set_person_or_company] = useState("Person")
    const navigate = useNavigate()
    
    const handle_time_interval = (interval: string) => {
        set_time_interval(interval)
        // console.log(time_interval)
    }
    

    // const handle_person_or_company = (value: string) => {
    //     // console.log("PERSON")
    //     // console.log(value)
    //     set_person_or_company(value)
    // }
    const css_class = 'homepage-overview-info-title'

    useEffect(() => {
        const fetchData = async () => {
            let transaction_result
            let ticker_result: Transaction[] | string[] | undefined
            if (transaction_type != null) {
              transaction_result = await retrieve_data(time_interval, transaction_type);
            } else {
              ticker_result = await retrieve_data(time_interval);
            }
            if (transaction_result && transaction_type != null) {
                set_top_transaction_data(transaction_result)
            } else if (ticker_result && transaction_type == null) {
                set_top_activity_tickers(ticker_result)
            }
        };

        fetchData();
    }, [time_interval]);

    let data_list_li
    if (transaction_type != null) {
      data_list_li = top_transaction_data.map((data_item: Transaction | string, index: number) => <li className={homepage_text_css} key={index} ><><a href={`${BASE_FRONTEND_URL}info/${(data_item as Transaction).reporting_owner_name.replace(/ /g, "%20")}`}>{(data_item as Transaction).reporting_owner_name}</a></></li>);
    } else {
      data_list_li = top_activity_tickers.map((data_item: Transaction | string, index: number) => <li className={homepage_text_css} key={index} ><><a href={`${BASE_FRONTEND_URL}info/${data_item}`}>{data_item as string}</a></></li>);
    }

    return (
        <div className={homepage_text_css}>
            <h3 className={css_class}>{title}</h3>
            <BasicMenu options={['Today','Week', 'Month', 'Year']} initial_title='Today' on_menu_change={handle_time_interval}/>
            {/* <BasicMenu options={['Person', 'Company']} initial_title='Person' on_menu_change={handle_person_or_company}/> */}
            <ol>
                {data_list_li}
            </ol>
        </div>
    )
}