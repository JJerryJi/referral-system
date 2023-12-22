import { useNavigate } from 'react-router-dom';
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

import { validateJobPostForm } from '../utils/validateForms';
import Scrollbar from '../components/scrollbar';

// ----------------------------------------------------------------------

export default function NewJobPage() {
  const navigate = useNavigate();
  const authToken = new Cookies().get('token');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isFormModified, setIsFormModified] = useState(false);

  // Initialize formData state to store form data
  const [formData, setFormData] = useState({
    job_name: '',
    job_company: '',
    job_requirement: '',
    job_question: '',
    job_description: '',
  });

  const handleFormChange = () => {
    setIsFormModified(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate the form fields
    const errors = validateJobPostForm(formData);

    if (Object.keys(errors).length === 0) {
      if(!isFormModified){
          setErrorMessage('You have already submitted a Referral Job Post with the same content. Please make changes before resubmitting.')
          setSuccessMessage('')
          return;
      }
      // proceed with form submission
      try {
        const response = await fetch('/job/api/posts', {
          method: 'POST',
          headers: {
            Authorization: authToken,
            'Content-Type': 'application/json', 
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();

        if (data.success) {
          // console.log('Referral Job Post submitted successfully');
          setSuccessMessage('Referral Job Post Successfully Submitted');
          setErrorMessage('');
          setIsFormModified(false);
          // navigate(`/dashboard/job-posts/${jobId}`);
        } else {
          setErrorMessage(data.error);
        }
      } catch (error) {
        // console.log(formData);
        console.error('Error:', error);
      }
    } else {
      // Validation errors found, display them
      setSuccessMessage('');
      setErrorMessage('Please correct the following form errors.\n'.concat(Object.values(errors).join('\n')));
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Use spread operator to update the specific field in formData
    setFormData({
      ...formData,
      [name]: value,
    });
    handleFormChange();
  };

  return (
    <>
      <Helmet>
        <title>Dashboard | Minimal UI</title>
      </Helmet>
      <Container style={{ maxWidth: '90%' }}>
        <Typography variant="h4" sx={{ mb: 5 }}>
          New Job Post
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={32} md={16} lg={16}>
            <Card>
              <CardHeader title="Content" />
              <CardContent>
                <Scrollbar>
                  <form onSubmit={handleSubmit} noValidate>
                    <FormControl fullWidth sx={{ mt: 0.75, mb: 3 }}>
                      <InputLabel> Job Post Name</InputLabel>
                      <Input
                        multiline
                        rows={1}
                        name="job_name"
                        value={formData.job_name}
                        onChange={handleChange}
                        required
                      />
                    </FormControl>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                      <InputLabel>Company</InputLabel>
                      <Input
                        multiline
                        rows={1}
                        name="job_company"
                        value={formData.job_company}
                        onChange={handleChange}
                        required
                      />
                    </FormControl>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                      <InputLabel>Requirement</InputLabel>
                      <Input
                        multiline
                        rows={2}
                        name="job_requirement"
                        value={formData.job_requirement}
                        onChange={handleChange}
                        required
                      />
                    </FormControl>
                    <FormControl fullWidth sx={{ mb: 3 }}>
                      <InputLabel>Description</InputLabel>
                      <Input
                        multiline
                        rows={2}
                        name="job_description"
                        value={formData.job_description}
                        onChange={handleChange}
                        required
                      />
                    </FormControl>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                      <InputLabel>Job Questions</InputLabel>
                      <Input
                        multiline
                        rows={2}
                        name="job_question"
                        value={formData.job_question}
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
                        Create A New Job Post
                      </LoadingButton>
                    </div>
                  </form>

                  <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
                    <LoadingButton
                      size="large"
                      variant="contained"
                      onClick={() => {
                        navigate(`/job-posts`);
                      }}
                    >
                      Back to All Job Posts
                    </LoadingButton>
                  </div>
                  {errorMessage && (
                    <Alert
                      sx={{ justifyContent: 'center', marginTop: '10px', whiteSpace: 'pre-wrap' }}
                      severity="error"
                    >
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
    </>
  );
}
