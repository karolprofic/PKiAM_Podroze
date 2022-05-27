import { React, useEffect } from 'react'
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button'
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
export default function MainPage() {
  const getData = async () => {
    const response = await axios.post(
      `http://localhost:5000/api/login`,
      {
        "username": "jan123",
        "password": "password"
      },
      { headers: { "Content-Type": "application/json" , }, withCredentials: true }
    )
    console.log(response.data)

  };
  useEffect(() => {
    getData();
  })
  const getInfo = async () => {
    const user = await axios.get(
      `http://localhost:5000/getUser`,
      { headers: { "Content-Type": "application/json" }, withCredentials: true }
    );
    console.log(user.data)
  }
  const zeroPad = (num, places) => String(num).padStart(places, '0')
  const dateToStringFormat = (date) => {
    return zeroPad(date.getFullYear(), 4) + '-' + zeroPad(date.getMonth() + 1, 2) + '-' + zeroPad(date.getDate(), 2)
  }
  const currentDate = new Date()
  const nextDate = new Date(Date.now() + 3600 * 1000 * 24)

  const getLink = (city, num, start, end) => {
    return `startingCity=${city};numberOfPeople=${num};startDate=${start};endDate=${end}`
  }

  let navigate = useNavigate();
  const redirect  = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log()
    const slug = getLink(data.get('city'), data.get('num'), data.get('dateFrom'), data.get('dateTo'))
    navigate(`/polecane/${slug}`)
  }

  return (
    <div className='main-page'>
      <h1>Zaplanuj swoją przygodę</h1>
      <h4>Wypełnij formularz i zobacz najciekawsze kierunki podróży</h4>
      <div className="form">
        <Box
          component="form"
          sx={{
            '& > :not(style)': { m: 1, width: '25ch' },
          }}
          onSubmit={redirect} 
          noValidate
          style={{ position: 'relative' }}
        >
          <TextField id="outlined-basic" label="Gdzie chcesz pojechać?" variant="outlined" name="city" style={{ width: '35ch' }} />
          <TextField id="outlined-basic" label="Ile osób?" variant="outlined" defaultValue="1" name="num" style={{ width: '10ch' }} />
          <TextField
            id="dateFrom"
            name="dateFrom"
            label="Od"
            type="date"
            defaultValue={dateToStringFormat(currentDate)}
          />
          <TextField
            id="dateTo"
            name="dateTo"
            label="Do"
            type="date"
            defaultValue={dateToStringFormat(nextDate)}
          />

          <Button type="submit" variant="contained" style={{ height: '56px' }}>Szukaj</Button>
        </Box>
      </div>
      <div className="login-buttons">
        <Link to='/logowanie'><Button variant="contained" style={{ height: '64px' }}>Zaloguj się</Button></Link>
        <Link to='/rejestracja'><Button variant="contained" style={{ height: '64px', marginLeft: '50px' }}>Zarejstruj się</Button></Link>
      </div>


    </div>
  )
}
