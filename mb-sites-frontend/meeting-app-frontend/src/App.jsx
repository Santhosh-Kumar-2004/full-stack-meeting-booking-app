import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Register from './pages/Register'

function App() {

  return (
    <>
      {/* <h1>Hello world</h1> */}
      <Router>
        {/* Navbar always visible */}
        {/* <Navbar /> */}

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
