import Navbar from '../components/Navbar'
import TransactionTable from '../components/TransactionTable'
import BarChart from '../components/BarChart'
import { Transaction } from '../components/types'
import { useParams } from 'react-router'
import { useEffect, useState } from 'react'

const BASE_API_URL = 'http://127.0.0.1:8000/api/'

async function get_transaction_row_data(search_query: string | undefined) {
    try {
      const response = await fetch(`${BASE_API_URL}common/transaction/${search_query}`)
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

export default function Info() {

  const { data } = useParams()
  // let transaction_data_rows: Transaction[] | undefined
  const [transaction_data_rows, set_transaction_data_rows] = useState<Transaction[]>([])

  useEffect(() => {
    console.log(`data value is: ${data}`)
    const fetchData = async () => {
        const transaction_data_rows_api = await get_transaction_row_data(data);
        if (transaction_data_rows_api) {
          set_transaction_data_rows(transaction_data_rows_api)
        }
        // console.log(transaction_data_rows)
    };

    fetchData();
  }, [data])

    return (
    <>
      <Navbar />
      <BarChart />
      <TransactionTable transaction_data={transaction_data_rows}/>
    </>
    )
}