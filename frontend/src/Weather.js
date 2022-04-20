import React from 'react'

export default function Weather({ weatherData }) {
    const convertUnixTimeToWeekDay = (time) => {
        let date = new Date(1000 * time)
        return date.toLocaleDateString('pl', { weekday: 'short' }); 
    }
    return (
        <div className='weather'>
            {
                weatherData.map(element => {
                    return (
                        <div style={{padding: '1em', textAlign: 'center', textTransform: 'uppercase'}}>
                            {convertUnixTimeToWeekDay(element.unixTime)}<br />
                            <span style={{color: '#d33100', fontWeight: 300}}>{Math.round(element.dayTemperature)} &deg;C</span>
                        </div>  
                    )
                })
            }
        </div>
    )
}
