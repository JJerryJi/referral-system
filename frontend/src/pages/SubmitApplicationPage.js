import { useParams, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useState } from 'react';
import Cookies from 'universal-cookie';

import {
  CardHeader,
  CardContent,
  Grid,
  Card,
  Container,
  Typography,
  FormControl,
  InputLabel,
  Input,
  Alert,
} from '@mui/material';
import { LoadingButton } from '@mui/lab';

import Scrollbar from '../components/scrollbar';

export default function SubmitApplicationPage() {
  const navigate = useNavigate();
  const authToken = new Cookies().get('token');
  const { jobId } = useParams();
  console.log(jobId);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Initialize formData state to store form data
  const [formData, setFormData] = useState({
    job_id: jobId,
    resume: null,
    linkedIn: '',
    answer: '',
  });

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;

    // Use spread operator to update the specific field in formData
    setFormData({
      ...formData,
      [name]: type === 'file' ? files[0] : value, // Use files[0] for file input
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create a new FormData object and append form data to it
    const formDataObject = new FormData();
    formDataObject.append('job_id', formData.job_id);
    formDataObject.append('resume', formData.resume);
    formDataObject.append('linkedIn', formData.linkedIn);
    formDataObject.append('answer', formData.answer);

    try {
      const response = await fetch('http://127.0.0.1:8000/application/api/application', {
        method: 'POST',
        headers: {
          Authorization: authToken,
        },
        body: formDataObject, // Using FormData for multipart/form-data,
      });

      // You can handle the response based on your requirements
      const data = await response.json();
      console.log('data:', data);

      // Optionally, you can navigate or perform other actions here
      if (data.success===true) {
        // console.log('Application submitted successfully');
        setSuccessMessage('Application submitted successfully');
        setErrorMessage('');
        // navigate(`/dashboard/job-posts/${jobId}`);
      } 
      else{
        setErrorMessage(data.error);
      }
    } catch (error) {
      console.error('Error:', error);
      throw new Error(error)
    }
  };

  return (
    <>
      <Helmet>
        <title>Dashboard | Minimal UI</title>
      </Helmet>
      <Container  style={{ maxWidth: "90%" }}>
        <Typography variant="h4" sx={{ mb: 5 }}>
          Apply for Job ID: {jobId}
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={32} md={16} lg={16}>
            <Card>
              <CardHeader title="Application" />
              <CardContent>
                <Scrollbar>
                  <form onSubmit={handleSubmit}>
                    <FormControl fullWidth sx={{ mb: 3 }}>
                      <Input type="file" name="resume" onChange={handleChange} required />
                    </FormControl>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                      <InputLabel>LinkedIn URL</InputLabel>
                      <Input type="url" name="linkedIn" value={formData.linkedIn} onChange={handleChange} required />
                    </FormControl>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                      <InputLabel>Answer</InputLabel>
                      <Input
                        multiline
                        rows={4}
                        name="answer"
                        value={formData.answer}
                        onChange={handleChange}
                        required
                      />
                    </FormControl>

                    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
                      <LoadingButton
                        type="submit"
                        size="large"
                        variant="contained"
                        // You can apply error style here based on your requirements
                      >
                        Apply
                      </LoadingButton>
                    </div>
                  </form>

                  <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
                    <LoadingButton
                      size="large"
                      variant="contained"
                      onClick={() => {
                        navigate(`/job-posts/`);
                      }}
                    >
                      Back to All Job Posts
                    </LoadingButton>
                  </div>
                  {errorMessage && (
                    <Alert sx={{ justifyContent: 'center', marginTop: '10px' }} severity="error">
                      {' '}
                      {errorMessage}
                    </Alert>
                  )}
                    {successMessage && (
                    <Alert sx={{ justifyContent: 'center', marginTop: '10px' }} >
                      {' '}
                      {successMessage}
                    </Alert>
                    
                  )}
                </Scrollbar>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
