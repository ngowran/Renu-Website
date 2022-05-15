import React, { Component } from "react";
import {render} from "react-dom";
import HomePage from "./HomePage";
import About from "./About";
import Contact from "./Contact";
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';

function App(props) {
    return (
        <Router>
            <Routes>
                <Route path='/' element={<HomePage/>} />
                <Route path='/about' element={<About/>} />
                <Route path='/contact' element={<Contact/>} />
            </Routes>      
         
        </Router>
    );
  }

export default App;

const appDiv = document.getElementById("app");
render(<App />, appDiv);