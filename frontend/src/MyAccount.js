import { React, useEffect, useState } from 'react'
import Navigation from './Navigation'
import axios from 'axios'
export default function MyAccount() {
    const [userData, setUserData] = useState({})
    const getUserData = async () => {
        const user = await axios.get(
            `http://localhost:5000/api/getUser`,
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        let temp = {}
        console.log(user.data)
        temp['userID'] = user.data[0][0]
        temp['firstName'] = user.data[0][1]
        temp['lastName'] = user.data[0][2]
        temp['city'] = user.data[0][3]
        temp['currency'] = user.data[0][4]
        temp['avatar'] = user.data[0][5]
        temp['username'] = user.data[0][6]

        setUserData(temp)
        console.log(temp)
    }

    useEffect(() => {
        getUserData()
    }, [])
    return (
        <div className='container'>
            <Navigation name='account' />
            <div className="recomendations">
                <img src={userData.avatar} alt="avatar" width={400} height={400} style={{ float: 'left', margin: '25px' }} /><br />
                <span style={{ display: 'block', fontSize: 40, fontWeight: 700, height: 250, lineHeight: '250px' }}>
                    {userData.firstName} {userData.lastName}
                </span>
                <div style={{ marginLeft: 250, fontSize: '24px'}}>
                    <strong>Miejscowość: </strong>{userData.city} <br />
                    <strong>Preferowana waluta:</strong> {userData.currency} <br />
                    <strong>Nazwa użytkownika:</strong> {userData.username} <br />

                </div>

            </div>
        </div>
    )
}
