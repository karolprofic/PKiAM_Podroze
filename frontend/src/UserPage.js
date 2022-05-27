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
    const [userData, setUserData] = useState({});
    const getData = async () => {
        const xd = parseQueryData(queryData)
        console.log(xd)
        const response = await axios.post(
            `http://localhost:5000/api/travelDestinations`,
            {
                "startingCity": "Warszawa",
                "weatherForecastDays": 10,
                "numberOfPeople": 1,
                "startDate": "2022-09-30",
                "endDate": "2022-10-01",
                "pageNumber": 1
            },
            { headers: { "Content-Type": "application/json"}, withCredentials: true }
        )
        console.log(response.data)
        setData(response.data)
    }
    const getUserData = () => {
        let temp = {
            favouritesLocations: new Set(['Warszawa', 'Praga', 'Wiedeń'])
        }
        setUserData(temp)
    }
    useEffect(() => {
        parseQueryData(queryData)
        getData()
        getUserData()
    }, [])

    const addToFavourites = (name) => {
        let temp = userData
        temp.favouritesLocations.add(name)
        setUserData(temp)
        console.log(userData)
        getData()
    }
    const removeFromFavourites = (name) => {
        let temp = userData
        temp.favouritesLocations.delete(name)
        setUserData(temp)
        console.log(userData)
        getData()
    }
    return (
        <div className='container'>
            <Navigation name='user-page' logged={true} />
            <div className="recomendations">
                {
                    data.map(element => {
                        return (
                            <div className='element'>
                                <div className="heart">
                                    {
                                        userData.favouritesLocations.has(element.name) ?
                                            <FontAwesomeIcon icon={faHeartCircleMinus} style={{ color: '#c0392b' }} onClick={() => removeFromFavourites(element.name)} /> :
                                            <FontAwesomeIcon icon={faHeartCirclePlus} onClick={() => addToFavourites(element.name)} />
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
                                    <span style={{ fontSize: 28 }}>Pogoda:<br /></span>
                                    <Weather weatherData={element.weather} />
                                </div>
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}
