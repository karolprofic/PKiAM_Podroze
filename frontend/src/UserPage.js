import { React, useState, useEffect } from 'react'
import Navigation from './Navigation'
import Weather from './Weather';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeartCircleMinus } from '@fortawesome/free-solid-svg-icons'
import { faHeartCirclePlus } from '@fortawesome/free-solid-svg-icons'
import { useParams } from 'react-router-dom';
import axios from 'axios';

export default function UserPage() {
    let { queryData } = useParams()

    const parseQueryData = (queryData) => {
        const args = queryData.split(';')
        const data = {}
        for (const arg of args) {
            const pair = arg.split('=')
            if (pair[0] === 'numberOfPeople')
                data[pair[0]] = parseInt(pair[1])
            else
                data[pair[0]] = pair[1]
        }
        data['weatherForecastDays'] = 10
        data['pageNumber'] = 1
        return data
    }

    const [data, setData] = useState([]);
    const [userData, setUserData] = useState({})
    const [queryInfo, setQueryInfo] = useState({})
    const [logged, setLogged] = useState(false)

    const getData = async () => {
        const query = parseQueryData(queryData)
        console.log(query)
        setQueryInfo(query)
        const response = await axios.post(
            `http://localhost:5000/api/travelDestinations`,
            query,
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        )
        console.log(response.data)
        setData(response.data)
    }
    const getUserData = async () => {
        const user = await axios.get(
            `http://localhost:5000/api/getUser`,
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        let temp = {}
        if (user.data.status === undefined) {
            console.log(user.data)
            temp['firstName'] = user.data[0][1]
            temp['lastName'] = user.data[0][2]
            temp['userID'] = user.data[0][0]

            const fav = await axios.post(
                `http://localhost:5000/api/getFavorites`,
                { "user_id": temp.userID },
                { headers: { "Content-Type": "application/json" }, withCredentials: true }
            );
            console.log(fav)
            let favouritesLocations = new Set()
            for (const element of fav.data) {
                favouritesLocations.add(element.name)
            }
            temp['favouritesLocations'] = favouritesLocations
            setUserData(temp)
            setLogged(true)
        }
        else {
            setUserData(user.data)
            console.log(user.data)
        }
    }

    useEffect(() => {
        parseQueryData(queryData)
        getData()
        getUserData()
    }, [])

    const addToFavourites = async (name) => {
        let temp = userData
        temp.favouritesLocations.add(name)
        setUserData(temp)
        console.log({
            "user_id": userData.userID,
            'city': name
        })
        const fav = await axios.post(
            `http://localhost:5000/api/addFavorites`,
            {
                "user_id": userData.userID,
                'city': name
            },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        console.log(fav)
        getData()
        // getUserData()
    }
    const removeFromFavourites = async (name) => {
        let temp = userData
        temp.favouritesLocations.delete(name)
        setUserData(temp)
        const fav = await axios.post(
            `http://localhost:5000/api/removeFavorite`,
            {
                "user_id": userData.userID,
                'city': name
            },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        console.log(fav)
        getData()
    }
    return (
        <div className='container'>
            <Navigation name='user-page' logged={logged} />
            <div className="recomendations">
                <div className='query-data'>
                    {
                        logged ? <>Witaj <strong>{userData.firstName} {userData.lastName}</strong> !<br /></> : null
                    }
                    <span style={{ fontSize: 20 }}>
                        Początkowa lokalizacja: {queryInfo.startingCity}<br />
                        Liczba osób: {queryInfo.numberOfPeople}<br />
                        Od: {queryInfo.startDate}<br />
                        Do: {queryInfo.endDate}<br />
                    </span>
                </div>
                {
                    data.map(element => {
                        return (
                            <>
                                <div className='element'>
                                    <div className="heart">
                                        {logged ?
                                            userData.favouritesLocations.has(element.name) ?
                                                <FontAwesomeIcon icon={faHeartCircleMinus} style={{ color: '#c0392b' }} onClick={() => removeFromFavourites(element.name)} /> :
                                                <FontAwesomeIcon icon={faHeartCirclePlus} onClick={() => addToFavourites(element.name)} /> : null
                                        }
                                    </div>
                                    <img src={element.imageURL} alt="" width={300} height={300} />
                                    <div className="info">
                                        <span style={{ fontSize: 36 }}>{element.name}<br /></span>
                                        <span style={{ fontSize: 28 }}>Informacje:<br /></span>
                                        <span style={{ fontSize: 20 }}>
                                            Odległość: {Math.round(element.distance)}km<br />
                                            Zachorowania na Covid-19: {element.covid.casesNew} <br />
                                        </span>
                                        <Weather weatherData={element.weather} />
                                    </div>
                                </div>
                                <div className='hotels'>
                                    {
                                        element.hotels.slice(0, 5).map(hotel => {
                                            return (
                                                <a href={hotel.url}>
                                                    <div className="hotel">
                                                        <img src={hotel.image} alt="" width={250} height={250} /> <br />
                                                        <span style={{ fontSize: 24, fontWeight: 700 }}>{hotel.name} </span><br />
                                                        {element.name} {hotel.address} <br /><br />
                                                        Ocena: <strong>{hotel.score}</strong><br />
                                                        Cena za noc: <strong>{hotel.price} {hotel.currency}</strong>
                                                    </div>
                                                </a>
                                            )
                                        })
                                    }
                                </div>
                            </>
                        )
                    })
                }
            </div>
        </div>
    )
}
