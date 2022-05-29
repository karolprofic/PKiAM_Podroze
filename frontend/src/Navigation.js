import React from 'react'
import { Link } from 'react-router-dom'
import logo from './logo.png'
import axios from 'axios'
export default function Navigation({ name, logged }) {
    const logOut = async () => {
        const response = await axios.post(
            `http://localhost:5000/api/logout`,
            {},
            { headers: { "Content-Type": "application/json" , }, withCredentials: true }
          )
          console.log(response.data)
    }
    return (
        <div className='navigation'>
            <img src={logo} alt="" width={200} />
            <nav>
                <ul className="menu">
                    <li className="item" >
                        <Link to='/'>Strona główna</Link>
                    </li>
                    <li className="item" style={logged === false ? { display: 'none' } : null}>
                        <Link to='/ulubione' style={name === 'favourites' ? { fontWeight: 700 } : null}>Ulubione</Link>
                    </li>
                    <li className="item" style={logged === false ? { display: 'none' } : null}>
                        <Link to='/konto' style={name === 'account' ? { fontWeight: 700 } : null}>Twoje konto</Link>
                    </li>
                    <li className="item" style={logged === false ? { display: 'none' } : null}>
                        <Link to='/' style={name === 'logOut' ? { fontWeight: 700 } : null} onClick={logOut}>Wyloguj się</Link>
                    </li>
                </ul>
            </nav>
        </div>
    )
}
