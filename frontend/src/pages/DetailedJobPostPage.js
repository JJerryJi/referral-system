import { useParams, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useEffect, useState } from 'react';
import { sentenceCase } from 'change-case';
import Cookies from 'universal-cookie';

import {
  Alert,
  CardHeader,
  CardContent,
  Grid,
  Card,
  Table,
  Stack,
  TableRow,
  TableBody,
  TableCell,
  Container,
  Typography,
  TableContainer,
} from '@mui/material';
import { LoadingButton } from '@mui/lab';

import { fDateTime } from '../utils/formatTime';
import Scrollbar from '../components/scrollbar';

export default function DetailedJobPostPage({ role }) {
  const navigate = useNavigate();
  const jobId = useParams().jobId;
  const student = role === 'student';
  // console.log(student);
  const authToken = new Cookies().get('token');
  const [jobPost, setJobPost] = useState({});
  const [errMsg, setErrMsg] = useState();
  const [successMsg, setSuccessMsg] = useState();

  const [applied, setApplied] = useState('');
  // const [favoriteJob, setFavoriteJob] = useState(null);
  console.log(authToken);

  useEffect(() => {
    // fetch job post info & if_applied
    fetch(`http://127.0.0.1:8088/job/api/posts/${jobId}`, {
      headers: {
        Authorization: authToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setApplied(data.has_student_applied_before);
        console.log(applied);
        setJobPost(data.job_post);
      })
      .catch((error) => {
        setErrMsg(error);
        console.log(error);
      });
  }, []);

  const hanldeFavoriteJob = () => {
    fetch(`http://127.0.0.1:8088/job/api/favorite_jobs`, {
      method: 'POST',
      headers: {
        Authorization: authToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ job_id: jobId }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.success === false) {
          setErrMsg(data.error);
          setSuccessMsg('');
        }
        else{
        // setFavoriteJob(true);
        setSuccessMsg(data.message);
        setErrMsg('');
        }
      })
      .catch((error) => {
        setErrMsg(error);
        console.log(error);
      });
  };
  const jobPostArray = Object.entries(jobPost);

  return (
    <>
      <Helmet>
        <title>Dashboard | Referral Finder</title>
      </Helmet>
      <Container maxWidth="xl">
        <Typography variant="h4" sx={{ mb: 5 }}>
          Here is the view of Job Post with ID: {jobId}
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={32} md={16} lg={16}>
            <Card>
              <CardHeader title="Job Post Details" />
              <CardContent>
                <Scrollbar>
                  <TableContainer sx={{ minWidth: 800 }}>
                    <Table>
                      <TableBody>
                        {jobPostArray.map(([key, value]) => {
                          // Exclude specific keys
                          if (key === 'alumni_id' || key === 'job_review_status' || key === 'job_id') {
                            return null; // Skip rendering this row
                          }
                          if (key === 'job_created_time') {
                            value = fDateTime(value)
                          }
                          const formattedKey = key
                            .split('_')
                            .map((word) => sentenceCase(word))
                            .join(' ');
                          return (
                            <TableRow hover key={key} tabIndex={-1}>
                              <TableCell component="th" scope="row" padding="none">
                                <Stack direction="row" alignItems="center" spacing={2}>
                                  <Typography variant="subtitle2" noWrap>
                                    {formattedKey}
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

                {student && (
                  <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                    <LoadingButton size="large" variant="contained" onClick={hanldeFavoriteJob}>
                      Add to Favorites
                    </LoadingButton>
                  </div>
                )}

                {!applied && <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
                  <LoadingButton
                    size="large"
                    variant="contained"
                    // disabled={applied}
                    onClick={() => {
                      navigate(`/application/${jobId}`);
                    }}
                  >
                    Apply for this Job
                  </LoadingButton>
                </div>}

                {applied && (
                  <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
                    <LoadingButton
                      size="large"
                      variant="contained"
                      onClick={() => {
                        navigate(`/application`);
                      }}
                    >
                      Go to Applications
                    </LoadingButton>
                  </div>
                )}

                {errMsg && (
                  <Alert sx={{ justifyContent: 'center', marginTop: '10px' }} severity="error">
                    {' '}
                    {errMsg}
                  </Alert>
                )}

                {successMsg && (
                  <Alert sx={{ justifyContent: 'center', marginTop: '10px' }} severity="success">
                    {' '}
                    {successMsg}
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
