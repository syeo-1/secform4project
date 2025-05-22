import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
// import Info from './pages/Info'
// import Home from './pages/Home'
import { BrowserRouter as Router, Route, Routes, Outlet } from 'react-router'
import { Suspense, lazy } from 'react';
import Loading from './components/Loading';

// example url with parameter: http://localhost:5173/info/reporting_owner/steve
// must include the parameter for the url to work!

// TODO: need to have some type of error page for invalid routes!
// or just redirect to Home??

const BASE_URL = 'http://127.0.0.1:8000/api/'

const Home = lazy(() => import('./pages/Home'));
const Info = lazy(() => import('./pages/Info'));

function Layout() {
  return (
    <div style={{
      backgroundColor: 'black',
      color: 'white',
      minHeight: '100vh',
      padding: '1rem'
    }}>
      <Outlet />
    </div>
  );
}

function App() {

  return (
    <Router>
      <Suspense fallback={<Loading/>}>
        <Routes>
          <Route path='/' element={<Home />}>
          </Route>
          <Route path='/info' element={<Info />}>
            <Route path=':data' element={<Info />}/>
            {/* <Route path='company_name/:company_name' element={<Info />}/>
            <Route path='ticker/:ticker' element={<Info />}/>
            <Route path='reporting_owner/:reporting_owner' element={<Info />}/> */}
          </Route>
        </Routes>
      </Suspense>
    </Router>
  )
}

export default App
