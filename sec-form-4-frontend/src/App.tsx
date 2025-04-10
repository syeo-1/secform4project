import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './components/Navbar'
import TransactionTable from './components/TransactionTable'
import BarChart from './components/BarChart'

function App() {
  return (
    <>
      <Navbar />
      <BarChart />
      <TransactionTable />
    </>
  )
}

export default App
