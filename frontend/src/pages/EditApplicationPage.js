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
  FormControl,
  InputLabel,
  Input,
  Link,
  Alert,
} from '@mui/material';
import { LoadingButton } from '@mui/lab';

import Scrollbar from '../components/scrollbar';

// ----------------------------------------------------------------------

export default function EditApplicationPage() {
  const { applicationId } = useParams();
  const navigate = useNavigate();
  const authToken = new Cookies().get('token');
  console.log(applicationId);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [resumeAvailable, setResumeAvailable] = useState(false);

  // Initialize formData state to store form data
  const [formData, setFormData] = useState({
    job_id: '',
    resume_path: null,
    linkedIn: '',
    answer: '',
  });

  useEffect(() => {
    // Fetch the existing application data and populate the form fields if needed
    async function fetchApplicationData() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/application/api/application/${applicationId}`, {
          headers: {
            Authorization: authToken,
          },
        });
        if (response.ok) {
          const data = await response.json();
          //   console.log("Data received from backend:", data);

          // populate the field with
          console.log(data);
          setFormData(data.application);
          if (data.application?.resume_path) {
            setResumeAvailable(true);
          }
        } else {
          const data = await response.json();
          console.log(data);
          setErrorMessage(data.error);
          setSuccessMessage('');
        }
      } catch (error) {
        console.log(error);
      }
    }

    fetchApplicationData();
  }, [applicationId, authToken]);

  const handleChange = (e) => {
    const { name, type } = e.target;

    if (type === 'file') {
      const file = e.target.files[0]; // Get the selected file
      if(file){
        setResumeAvailable(false);
        setFormData({
          ...formData,
          [name]: file, // Attach the file to the corresponding field in formData
        });
      }
    } else {
      // Handle other form fields (e.g., text input, textarea) here
      const { value } = e.target;
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create a new FormData object and append form data to it
    const formDataObject = new FormData();
    formDataObject.append('job_id', formData.job_id);
    formDataObject.append('resume', formData.resume_path);
    formDataObject.append('linkedIn', formData.linkedIn);
    formDataObject.append('answer', formData.answer);

    try {
      const response = await fetch(`http://127.0.0.1:8000/application/api/application/${applicationId}`, {
        method: 'PUT',
        headers: {
          Authorization: authToken,
        },
        body: formDataObject, // Using FormData for multipart/form-data,
      });
      const data = await response.json();
      console.log('data:', data);

      if (data.success === true) {
        console.log('Update of Your Application submitted successfully');
        setSuccessMessage(data.message);
        setErrorMessage('');
      } else {
        setErrorMessage(data.error);
        setSuccessMessage('');
      }
    } catch (error) {
      console.log(error);
      throw new Error(error);
    }
  };

  return (
    <Container style={{ maxWidth: '90%' }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Modify Application ID: {applicationId}
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={32} md={16} lg={16}>
          <Card>
            <CardHeader title="Application" />
            <CardContent>
              <Scrollbar>
                {resumeAvailable && (
                  <Link
                    href={`http://127.0.0.1:8000/${formData.resume_path}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{ mb: 2 }}
                  >
                    Preview Previous Resume
                  </Link>
                )}
                <form onSubmit={handleSubmit}>
                  <FormControl fullWidth sx={{ mb: 3, mt: 1 }}>
                    <Input type="file" name="resume_path" accept=".pdf" onChange={handleChange} required />
                  </FormControl>

                  <FormControl fullWidth sx={{ mb: 3 }}>
                    <InputLabel>LinkedIn URL</InputLabel>
                    <Input type="url" name="linkedIn" value={formData.linkedIn} onChange={handleChange} required />
                  </FormControl>

                  <FormControl fullWidth sx={{ mb: 3 }}>
                    <InputLabel>Answer</InputLabel>
                    <Input multiline rows={4} name="answer" value={formData.answer} onChange={handleChange} required />
                  </FormControl>

                  <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
                    <LoadingButton
                      type="submit"
                      size="large"
                      variant="contained"
                      // You can apply error style here based on your requirements
                    >
                      Modify this Application
                    </LoadingButton>
                  </div>
                </form>

                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
                  <LoadingButton
                    size="large"
                    variant="contained"
                    onClick={() => {
                      navigate(`/application`);
                    }}
                  >
                    Back to All Applications
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
              </Scrollbar>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}
