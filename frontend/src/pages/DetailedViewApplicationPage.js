import { useParams, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useState, useEffect } from 'react';
import Cookies from 'universal-cookie';

import {
  CardHeader,
  CardContent,
  Grid,
  Card,
  Container,
  Typography,
  Alert,
  TableCell,
  TableBody,
  TableRow,
  Stack,
  TableContainer,
  Table,
} from '@mui/material';
import { LoadingButton } from '@mui/lab';
import { sentenceCase } from 'change-case';

import Scrollbar from '../components/scrollbar';
import { fDateTime } from '../utils/formatTime';

// ----------------------------------------------------------------------

export default function DetailedViewApplicationPage() {
  const { applicationId } = useParams();
  const authToken = new Cookies().get('token');
  console.log(applicationId);
  const [application, setApplication] = useState([]);
  const [applicant, setApplicant] = useState([]);
  const [applicantUser, setApplicantUser] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  useEffect(() => {
    // get application data
    fetch(`/application/api/application/${applicationId}`, {
      headers: {
        Authorization: authToken,
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        // console.log(data.application);
        setApplication(data.application);

        if (data.application.student_id) {
          fetch(`/user/api/student/${data.application.student_id}`)
            .then((studentResponse) => {
              return studentResponse.json();
            })
            .then((data2) => {
              if (data2.student.user) setApplicantUser(data2.student.user);
              setApplicant(data2.student);
            });
        } else {
          setErrorMessage('Applicant Student ID is not found!');
        }
      })
      .catch((error) => {
        setErrorMessage(error);
        console.log(error);
      });
    // get applicant data
  }, []);

  const applicationArray = Object.entries(application);
  const applicantArray = Object.entries(applicant);
  const userArray = Object.entries(applicantUser);

  // Handler for the "Select this Application" button
  const handleSelectApplication = (status) => {
    // Send the PUT request to update the application status
    fetch(`/application/api/application/${applicationId}`, {
      method: 'PUT',
      headers: {
        Authorization: authToken, // Add your authorization token here
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"status": status }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to update application status');
        }
        return response.json();
      })
      .then((data) => {
        if (data.success === true) {
          setSuccessMessage(data.message);
          setErrorMessage('');
        } else {
          setErrorMessage(data.error);
          setSuccessMessage('');
        }
      })
      .catch((error) => {
        // Handle errors, e.g., show an error message to the user
        setErrorMessage(error.message);
        setSuccessMessage('');
      });
  };

  const handleSelection = () => {
    handleSelectApplication('Selected');
    console.log('selected');
  };

  const handleReject = () => {
    handleSelectApplication('Not-moving-forward');
  };

  return (
    <>
      <Helmet>
        <title> Referral_Finder </title>
      </Helmet>
      <Container maxWidth="xl">
        <Typography variant="h4" sx={{ mb: 5 }}>
          Application {applicationId}:
        </Typography>
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={32} md={16} lg={16}>
            <Card>
              <CardHeader title="Application Details" />
              <CardContent>
                <Scrollbar>
                  <TableContainer sx={{ minWidth: 800 }}>
                    <Table>
                      <TableBody>
                        {applicationArray.map(([key, value]) => {
                          // Exclude specific keys
                          if (
                            key === 'student_id' ||
                            key === 'job_review_status' ||
                            key === 'job_name' ||
                            key === 'job_id'
                          ) {
                            return null; // Skip rendering this row
                          }
                          if (key === 'application_date' || key === 'modified_date') {
                            value = fDateTime(value);
                          }

                          return (
                            <TableRow hover key={key} tabIndex={-1}>
                              <TableCell component="th" scope="row" padding="none">
                                <Stack direction="row" alignItems="center" spacing={2}>
                                  <Typography variant="subtitle2" noWrap>
                                    {key !== 'linkedIn' ? sentenceCase(key) : key}
                                  </Typography>
                                </Stack>
                              </TableCell>
                              <TableCell align="left" sx={{ whiteSpace: 'pre-wrap' }}>
                                {key === 'resume_path' ? (
                                  <a href={`http://localhost:8088${value}`} target="_blank" rel="noopener noreferrer">
                                    Preview Resume
                                  </a>
                                ) : (
                                  value
                                )}
                              </TableCell>
                            </TableRow>
                          );
                        })}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Scrollbar>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Grid container spacing={3}>
          <Grid item xs={32} md={16} lg={16}>
            <Card>
              <CardHeader title="Applicant Details" />
              <CardContent>
                <Scrollbar>
                  <TableContainer sx={{ minWidth: 800 }}>
                    <Table>
                      <TableBody>
                        {userArray.map(([key, value]) => {
                          // Exclude specific keys
                          if (key === 'id' || key === 'username') {
                            return null; // Skip rendering this row
                          }
                          if (key === 'graduation_year') {
                            value = fDateTime(value).split(' ').slice(1, -2).join(' ');
                          }
                          return (
                            <TableRow hover key={key} tabIndex={-1}>
                              <TableCell component="th" scope="row" padding="none">
                                <Stack direction="row" alignItems="center" spacing={2}>
                                  <Typography variant="subtitle2" noWrap>
                                    {key !== 'linkedIn' ? sentenceCase(key) : key}
                                  </Typography>
                                </Stack>
                              </TableCell>
                              <TableCell align="left" sx={{ whiteSpace: 'pre-wrap' }}>
                                {value}
                              </TableCell>
                            </TableRow>
                          );
                        })}

                        {applicantArray.map(([key, value]) => {
                          // Exclude specific keys
                          if (key === 'user' || key === 'student_id') {
                            return null; // Skip rendering this row
                          }
                          if (key === 'graduation_year') {
                            value = fDateTime(value).split(' ').slice(1, -2).join(' ');
                          }
                          return (
                            <TableRow hover key={key} tabIndex={-1}>
                              <TableCell component="th" scope="row" padding="none">
                                <Stack direction="row" alignItems="center" spacing={2}>
                                  <Typography variant="subtitle2" noWrap>
                                    {key !== 'linkedIn' ? sentenceCase(key) : key}
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

                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                  <LoadingButton
                    size="large"
                    variant='contained'
                    color="success"
                    value="success"
                    onClick={handleSelection}
                  >
                    Select this Application
                  </LoadingButton>
                </div>

                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                  <LoadingButton
                    size="large"
                    variant='contained'
                    color="error"
                    value="Fail"
                    onClick={handleReject}
                  >
                    Fail this Application
                  </LoadingButton>
                </div>

                {errorMessage && (
                  <Alert sx={{ justifyContent: 'center', marginTop: '10px' }} severity="error">
                    {' '}
                    {errorMessage}
                  </Alert>
                )}
                {successMessage && (
                  <Alert sx={{ justifyContent: 'center', marginTop: '10px' }}> {successMessage}</Alert>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
