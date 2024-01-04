import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'universal-cookie';

// @mui
import { alpha } from '@mui/material/styles';
import { Box, Divider, Typography, Stack, MenuItem, Avatar, IconButton, Popover } from '@mui/material';
// mocks_
import account from '../../../_mock/account';

// ----------------------------------------------------------------------

const MENU_OPTIONS = [
  {
    label: 'Home',
    icon: 'eva:home-fill',
  },
  {
    label: 'Profile',
    icon: 'eva:person-fill',
  },
];

// ----------------------------------------------------------------------

export default function AccountPopover() {
  const cookies = new Cookies();
  const token = cookies.get('token')?.split(' ')[1];

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [error, setErrorMsg] = useState('');

  useEffect(() => {
    fetch(`/api/token?token=${token}`, {
      method: 'GET',
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data.email) {
          setEmail(data.email);
        }
        if (data.username) {
          setUsername(data.username);
        }
        // console.log(data);
        // console.log(username);
        // console.log(email);
      })
      .catch((error) => {
        setErrorMsg(error);
        throw new Error(error);
      });
  });

  // fetch user email
  const navigate = useNavigate();
  const [open, setOpen] = useState(null);

  const handleOpen = (event) => {
    setOpen(event.currentTarget);
    // console.log(open);
  };

  const handleClose = ()=>{
    setOpen(null);
  };

  const handleCloseProfile = () => {
    setOpen(null);
    navigate('/profile')
  };

  const hanldeCloseHome = () => {
    setOpen(null);
    navigate('/job-posts');
  };

  return (
    <>
      <IconButton
        onClick={handleOpen}
        sx={{
          p: 0,
          ...(open && {
            '&:before': {
              zIndex: 1,
              content: "''",
              width: '100%',
              height: '100%',
              borderRadius: '50%',
              position: 'absolute',
              bgcolor: (theme) => alpha(theme.palette.grey[900], 0.8),
            },
          }),
        }}
      >
        <Avatar src={account.photoURL} alt="photoURL" />
      </IconButton>

      <Popover
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            p: 0,
            mt: 1.5,
            ml: 0.75,
            width: 180,
            '& .MuiMenuItem-root': {
              typography: 'body2',
              borderRadius: 0.75,
            },
          },
        }}
      >
        <Box sx={{ my: 1.5, px: 2.5 }}>
          {username === '' ? (
            <>
              <Typography variant="subtitle2" noWrap color="error">
                Unauthorized user
              </Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
                Please sign in now
              </Typography>
            </>
          ) : (
            <>
              <Typography variant="subtitle2" noWrap>
                {username}
              </Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
                {email}
              </Typography>
            </>
          )}
        </Box>

        <Divider sx={{ borderStyle: 'dashed' }} />

        <Stack sx={{ p: 1 }}>
          <MenuItem key={MENU_OPTIONS[0].label} onClick={hanldeCloseHome}>{MENU_OPTIONS[0].label}</MenuItem>
          <MenuItem key={MENU_OPTIONS[1].label} onClick={handleCloseProfile}>{MENU_OPTIONS[1].label}</MenuItem>

        </Stack>

        <Divider sx={{ borderStyle: 'dashed' }} />

        {/* Logout logic: */}
        <MenuItem
          onClick={() => {
            handleClose();
            navigate('/login');
            cookies.remove('token', { path: '/' });
            // console.log(cookies.get('token'));
          }}
          sx={{ m: 1 }}
        >
          Logout
        </MenuItem>
      </Popover>
    </>
  );
}
