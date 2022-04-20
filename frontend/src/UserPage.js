import { React, useState, useEffect } from 'react'
import Navigation from './Navigation'
import Weather from './Weather';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeartCircleMinus } from '@fortawesome/free-solid-svg-icons'
import { faHeartCirclePlus } from '@fortawesome/free-solid-svg-icons'

export default function UserPage() {

    const [data, setData] = useState([]);
    const [userData, setUserData] = useState({});
    const getData = () => {
        fetch('destinations.json'
            , {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }
        )
            .then(function (response) {
                console.log(response)
                return response.json();
            })
            .then(function (myJson) {
                console.log(myJson);
                setData(myJson)
            });
    }
    const getUserData = () => {
        let temp = {
            favouritesLocations: new Set(['Warszawa', 'Praga', 'Wiedeń'])
        }
        setUserData(temp)
    }
    useEffect(() => {
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
                                        <FontAwesomeIcon icon={faHeartCircleMinus} style={{color: '#c0392b'}} onClick={() => removeFromFavourites(element.name)}/> :
                                        <FontAwesomeIcon icon={faHeartCirclePlus} onClick={() => addToFavourites(element.name)}/>
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
