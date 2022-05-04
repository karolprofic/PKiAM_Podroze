import { React, useEffect } from 'react'
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Autocomplete from '@mui/material/Autocomplete';
import axios from 'axios';
export default function MainPage() {
  const getData = async () => { 
    const response = await axios.post(
      `http://${window.location.hostname}:5000/login/`,
      {
        "username": "jan123",
        "password": "password"
      },
      { headers: { "Content-Type": "application/json" } }
    )
    console.log(response.data)

  };
  useEffect(() => {
    getData();
  })
  const login = async () => {
    const user = await axios.get(
      `http://${window.location.hostname}:5000/user/`,
      { "username": "jan123" }
    );
    console.log(user.data)
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

          style={{ position: 'relative' }}
        >
          <TextField id="outlined-basic" label="Gdzie chcesz pojechać?" variant="outlined" />
          <Autocomplete
            id="combo-box-demo"
            options={[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
            renderInput={(params) => <TextField {...params} label="Liczba" />}
          />
          <TextField
            id="date"
            label="Od"
            type="date"
            defaultValue="2022-05-24"
          />
          <TextField
            id="date"
            label="Do"
            type="date"
            defaultValue="2022-05-24"
          />

          <Button onClick={login} variant="contained" style={{ height: '56px' }}>Szukaj</Button>
        </Box>
      </div>
    </div>
  )
}
