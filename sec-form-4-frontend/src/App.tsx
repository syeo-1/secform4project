import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Info from './pages/Info'
import Home from './pages/Home'
import { BrowserRouter as Router, Route, Routes } from 'react-router'

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />}>
        </Route>
        <Route path='/info' element={<Info />}>
        </Route>
      </Routes>
    </Router>
  )
}

export default App
