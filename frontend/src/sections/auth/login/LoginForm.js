import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from "universal-cookie";
// @mui
import { Link, Stack, IconButton, InputAdornment, TextField, Alert } from '@mui/material';
import { LoadingButton } from '@mui/lab';
// components
import Iconify from '../../../components/iconify';


export default function LoginForm() {
  const cookies = new Cookies();
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [message, setMessage] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleClick = async () => {
    try {
      const response = await fetch('/api/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });

      if (response.ok) {
        // Successful login, you can perform any necessary actions here.
        // For example, you can redirect the user to the dashboard.
        const data = await response.json()
        cookies.set('token', `Token ${data.token}`, { path: '/'});
        navigate('/job-posts');

      } else {
        // Handle login failure, display an error message, etc.
        console.error('Login failed');
        setMessage('Login Failed');
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }
  };

  return (
    <>
      <Stack spacing={3}>
        <TextField
          name="username"
          label="Username"
          value={formData.username}
          onChange={handleInputChange}
        />

        <TextField
          name="password"
          label="Password"
          type={showPassword ? 'text' : 'password'}
          value={formData.password}
          onChange={handleInputChange}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                  <Iconify icon={showPassword ? 'eva:eye-fill' : 'eva:eye-off-fill'} />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      </Stack>

      <Stack  alignItems="center" sx={{ my: 1 }}>
        <Link variant="subtitle2" underline="hover" onClick={()=>navigate('/signup')}>
          Sign up here
        </Link>
      </Stack>

      <LoadingButton fullWidth size="large" type="submit" variant="contained" onClick={handleClick}>
        Login
      </LoadingButton>

    {message === 'Login Failed' && <Alert sx={{ justifyContent: 'center', marginTop: '10px' }}>{message}</Alert> }
    </>
  );
}
