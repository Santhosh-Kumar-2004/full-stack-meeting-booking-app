import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Register from './pages/Register'

function App() {

  return (
    <>
      {/* <h1>Hello world</h1> */}
      <Register />
    </>
  )
}

export default App
