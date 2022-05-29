import React from 'react'

export default function Weather({ weatherData }) {
    const convertUnixTimeToWeekDay = (time) => {
        let date = new Date(1000 * time)
        return date.toLocaleDateString('pl', { weekday: 'short' }); 
    }
    const getWeatherIcon = (weather) => {
        switch (weather) {
            case 'Clouds':
                return 'http://openweathermap.org/img/wn/03d@2x.png'
            case 'Clear':
                return 'http://openweathermap.org/img/wn/01d@2x.png'
            case 'Rain':
                return 'http://openweathermap.org/img/wn/09d@2x.png'
            case 'Snow':
                return 'http://openweathermap.org/img/wn/13d@2x.png'
            default:
                return 'http://openweathermap.org/img/wn/02d@2x.png'
        }
    }
    return (
        <div className='weather'>
            {
                weatherData.map(element => {
                    return (
                        <div style={{padding: '1em', textAlign: 'center', textTransform: 'uppercase', background:'#bdc3c7', margin: '0.2em', borderRadius: 5}}>
                            {convertUnixTimeToWeekDay(element.unixTime)}<br />
                            <img src={getWeatherIcon(element.weatherIcon)} alt="" height={50} width={50}/><br />
                            <span style={{color: '#d33100', fontWeight: 300}}>{Math.round(element.dayTemperature)} &deg;C</span>
                        </div>  
                    )
                })
            }
        </div>
    )
}
