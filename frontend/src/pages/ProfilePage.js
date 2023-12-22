import { Helmet } from 'react-helmet-async';
import { sentenceCase } from 'change-case';
import Cookies from 'universal-cookie';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// @mui
import {
  Card,
  Table,
  Stack,
  Paper,
  Avatar,
  Button,
  Popover,
  Checkbox,
  TableRow,
  MenuItem,
  TableBody,
  TableCell,
  Container,
  Typography,
  IconButton,
  TableContainer,
  TablePagination,
} from '@mui/material';
// components
import Label from '../components/label';
import Scrollbar from '../components/scrollbar';
// sections
import { UserListHead } from '../sections/@dashboard/user';
import { fDateTime } from '../utils/formatTime';

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: 'fields', label: 'Fields', alignRight: false },
  { id: 'user_info', label: 'User Profile Data', alignRight: false },
];

// ----------------------------------------------------------------------

export default function ProfilePage() {
  const cookies = new Cookies();
  const token = cookies.get('token');
  const tokenNumber = token?.split(' ')[1];
  const [profileData, setProfileData] = useState([]);
  const [error, setErrorMsg] = useState('');

  useEffect(() => {
    async function fetchProfile() {
      try {
        const response = await fetch(`/api/token?token=${tokenNumber}`, {
          method: 'GET'
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data);
        let studentResponse = null;
        let alumniResponse = null;
        if (data.alumni_id) {
          alumniResponse = await fetch(`/user/api/alumni/${data.alumni_id}`, {
            method: 'GET',
            headers: { Authorization: token },
          });
        } else if (data.student_id) {
          studentResponse = await fetch(`/user/api/student/${data.student_id}`, {
            method: 'GET',
            headers: { Authorization: token },
          });
        } else {
          setErrorMsg('No Student or Alumni ID is found');
        }

        if (alumniResponse) {
          const userData = await alumniResponse.json();
          console.log(userData);
          setProfileData(userData.alumni);
        } else if (studentResponse) {
          const userData = await studentResponse.json();
          console.log(userData.student);
          setProfileData(userData.student);
        }
      } catch (error) {
        setErrorMsg('Error fetching profile ID');
        console.error('Error fetching profile ID:', error);
      }
    }
    fetchProfile();
  }, [tokenNumber]);

  const profileDataArray = Object.entries(profileData);

  return (
    <>
      <Helmet>
        <title> User | Referral_Finder </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            My Profile
          </Typography>
        </Stack>

        <Card>
          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>
              <Table>
                <UserListHead headLabel={TABLE_HEAD} />
                <TableBody>
                  {profileData.user &&
                    Object.entries(profileData.user).map(([key, value]) => {
                      // Exclude specific keys
                      if (key === 'id' || key === 'password') {
                        return null;
                      }
                      return (
                        <TableRow hover key={key} tabIndex={-1}>
                          <TableCell component="th" scope="row" sx={{paddingLeft:2}}>
                            <Stack direction="row" alignItems="center" spacing={2}>
                              <Typography variant="subtitle2" noWrap>
                                {sentenceCase(key)}
                              </Typography>
                            </Stack>
                          </TableCell>
                          <TableCell align="left" sx={{ whiteSpace: 'pre-wrap' }}>
                            {value}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  {profileDataArray.map(([key, value]) => {
                    // Exclude specific keys
                    if (key === 'user' || key === 'student_id' || key === 'alumni_id' || key === 'modified_time'  ) {
                      return null; // Skip rendering this row
                    }

                    if (key === 'graduation_year') {
                      value = fDateTime(value).split(' ').slice(1, 3).join(' ');
                    }
                    if (key === 'created_time') {
                      value = fDateTime(value);
                    }
                    return (
                      <TableRow hover key={key} tabIndex={-1}>
                        <TableCell component="th" scope="row" sx={{paddingLeft:2}} >
                          <Stack direction="row" alignItems="center" spacing={2}>
                            <Typography variant="subtitle2" noWrap>
                              {sentenceCase(key)}
                            </Typography>
                          </Stack>
                        </TableCell>
                        <TableCell align="left" sx={{ whiteSpace: 'pre-wrap' }}>
                          {value}
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </TableContainer>
          </Scrollbar>
        </Card>
      </Container>
    </>
  );
}
