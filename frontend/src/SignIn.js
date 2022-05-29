import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from "axios";
import { Link as RootLink, useNavigate } from "react-router-dom";
const theme = createTheme();

export default function SignIn() {
  let navigate = useNavigate();
  const redirect = () => {
    navigate(`/`)
  };
  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    // eslint-disable-next-line no-console
    const loginData = {
      'username': data.get('email'),
      'password': data.get('password'),
    }
    console.log(loginData);
    const response = await axios.post(
      `http://localhost:5000/api/login`,
      loginData,
      { headers: { "Content-Type": "application/json", }, withCredentials: true }
    ).then(redirect).catch((reason) => {
      window.alert('Wrong username or password!')
    })
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h1">
            SuperTravel
          </Typography>
          <Typography component="h1" variant="h5">
            Zaloguj się
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Nazwa użytkownika"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Hasło"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Zaloguj się
            </Button>
            <Grid container>
              <Grid item xs>
              </Grid>
              <Grid item>
                <Link variant="body2">
                  <RootLink to="/rejestracja">
                    {"Nie masz konta? Zarejestruj się"}
                  </RootLink>
                </Link>
                <br />
                <Link variant="body2">
                  <RootLink to="/">
                    {"Powrót do strony głównej"}
                  </RootLink>
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}