import Navbar from '../components/Navbar'
import TransactionTable from '../components/TransactionTable'
import BarChart from '../components/BarChart'
import { Transaction } from '../components/types'
import { useParams } from 'react-router'
import { useEffect } from 'react'

const BASE_API_URL = 'http://127.0.0.1:8000/api/'

async function get_transaction_row_data(search_query: string) {
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

  const transaction_data_rows = []
  const { data } = useParams()

  useEffect(() => {
    console.log(`data value is: ${data}`)
  }, [])

    return (
    <>
      <Navbar />
      <BarChart />
      <TransactionTable />
    </>
    )
}