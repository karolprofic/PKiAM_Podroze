import React from 'react'
import { Link } from 'react-router-dom'
import logo from './logo.png'
export default function Navigation({ name, logged }) {
    return (
        <div className='navigation'>
            <img src={logo} alt="" width={200} />
            <nav>
                <ul className="menu">
                    <li className="item" >
                        <Link to='/'>Strona główna</Link>
                    </li>
                    <li className="item" >
                        <Link to='/polecane' style={name === 'user-page' ? { fontWeight: 700 } : null}>Polecane</Link>
                    </li>
                    <li className="item" style={logged === false ? { display: 'none' } : null}>
                        <Link to='/ulubione' style={name === 'favourites' ? { fontWeight: 700 } : null}>Ulubione</Link>
                    </li>
                    <li className="item" style={logged === false ? { display: 'none' } : null}>
                        <Link to='/konto' style={name === 'account' ? { fontWeight: 700 } : null}>Twoje konto</Link>
                    </li>
                </ul>
            </nav>
        </div>
    )
}
