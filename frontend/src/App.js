import './styles/main.css';
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import UserPage from './UserPage';
import MainPage from './MainPage';
import MyAccount from './MyAccount';
import Favourites from './Favourites';
import SignIn from './SignIn';
import SignUp from './SignUp';
export default function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<MainPage />} />
        <Route exact path="/polecane/:queryData" element={<UserPage />} />
        <Route exact path="/konto/" element={<MyAccount />} />
        <Route exact path="/ulubione/" element={<Favourites />} />
        <Route exact path="/logowanie/" element={<SignIn />} />
        <Route exact path="/rejestracja/" element={<SignUp />} />
      </Routes>
    </Router>

  )
}

