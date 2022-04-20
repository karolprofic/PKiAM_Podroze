import './styles/main.css';
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import UserPage from './UserPage';
import MainPage from './MainPage';
import MyAccount from './MyAccount';
import Favourites from './Favourites';
export default function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<MainPage />} />
        <Route exact path="/polecane/" element={<UserPage />} />
        <Route exact path="/konto/" element={<MyAccount />} />
        <Route exact path="/ulubione/" element={<Favourites />} />
      </Routes>
    </Router>

  )
}

