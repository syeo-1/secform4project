import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Info from './pages/Info'
import Home from './pages/Home'
import { BrowserRouter as Router, Route, Routes } from 'react-router'

// example url with parameter: http://localhost:5173/info/reporting_owner/steve
// must include the parameter for the url to work!

// TODO: need to have some type of error page for invalid routes!
// or just redirect to Home??

const BASE_URL = 'http://127.0.0.1:8000/api/'

function App() {

  const ticker = "BTCS"
  // fetch(`${BASE_URL}ticker/${ticker}`)
  //   .then(res => {
  //     if (res.ok) {
  //       console.log('success')
  //     } else {
  //       console.log('not successful')
  //     }
  //   })
  //   .then(data => console.log(data))
  //   .catch(error => console.log(error))

  const get_ticker_info  = async () => {
    try {
      const response = await fetch(`${BASE_URL}ticker/${ticker}`)
      const data = await response.json()
      console.log(data)
    } catch(error) {
      console.log(error)
    }
  }

  get_ticker_info()

  
  // console.log(fetch(`${BASE_URL}ticker/${ticker}`))
  
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />}>
        </Route>
        <Route path='/info' element={<Info />}>
          <Route path='company_name/:company_name' element={<Info />}/>
          <Route path='ticker/:ticker' element={<Info />}/>
          <Route path='reporting_owner/:reporting_owner' element={<Info />}/>
        </Route>
      </Routes>
    </Router>
  )
}

export default App
