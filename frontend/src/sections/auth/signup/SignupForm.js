import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
// @mui
import { TextField, Select, MenuItem, FormControl, InputLabel, Stack, Alert, Link } from '@mui/material';
import { LoadingButton } from '@mui/lab';

import { validateSignUpForm } from '../../../utils/validateForms';

export default function SignupForm() {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    location: '',
    email: '',
    first_name: '',
    last_name: '',
    role: '',
    school: '',
    year_in_school: '',
    major: '',
    degree: '',
    graduation_year: '',
    year: '',
    graduation_month: '',
    company_name: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 6 }, (_, i) => currentYear + i);
  const months = Array.from({ length: 12 }, (_, i) => i + 1);
  const yearsInSchool = [1, 2, 3, 4, 5]; 

  const handleSubmit = () => {
    // validate the form before submitting
    const errors = validateSignUpForm(formData);
    // console.log(result);
    if (Object.values(errors).length === 0) {
      // Combine graduation_year and graduation_month into a date-time string
      formData.graduation_year = `${formData.year}-${String(formData.graduation_month).padStart(2, '0')}-01T00:00:00`;

      console.log(formData);

      // call backend API according to user type
      fetch(`http://127.0.0.1:8088/user/api/${formData.role}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...formData }),
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          // console.log(data);
          if (!data.success) {
            setSuccessMessage(null);
            setErrorMessage(data.error);
          } else if (data.success) {
            setSuccessMessage(data.message);
            console.log(successMessage);
            setErrorMessage(null);
          }
          // navigate('/login');
        });
    } else {
      setErrorMessage('Please correct the following form errors:\n'.concat(Object.values(errors).join('\n')));
    }
  };

  return (
    <>
      <Stack spacing={2}>
        <TextField name="username" label="Username" value={formData.username} onChange={handleInputChange} fullWidth />
        <TextField name="password" label="Password" value={formData.password} onChange={handleInputChange} fullWidth />
        <TextField name="email" label="email" value={formData.email} onChange={handleInputChange} fullWidth />
        <TextField name="location" label="Location" value={formData.location} onChange={handleInputChange} fullWidth />
        <TextField
          name="first_name"
          label="First Name"
          value={formData.first_name}
          onChange={handleInputChange}
          fullWidth
        />
        <TextField
          name="last_name"
          label="Last Name"
          value={formData.last_name}
          onChange={handleInputChange}
          fullWidth
        />
        <FormControl fullWidth>
          <InputLabel>User Type</InputLabel>
          <Select name="role" value={formData.role} onChange={handleInputChange} label="User Type" fullWidth>
            <MenuItem value="student">Student</MenuItem>
            <MenuItem value="alumni">Alumni</MenuItem>
          </Select>
        </FormControl>
        {formData.role === 'student' && (
          <Stack spacing={1.5}>
            <TextField name="school" label="School" value={formData.school} onChange={handleInputChange} fullWidth />
            <FormControl fullWidth>
              <InputLabel>Year in School</InputLabel>
              <Select
                name="year_in_school"
                value={formData.year_in_school}
                onChange={handleInputChange}
                label="Year in School"
                fullWidth
              >
                {yearsInSchool.map((year) => (
                  <MenuItem key={year} value={year}>
                    {year}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField name="major" label="Major" value={formData.major} onChange={handleInputChange} fullWidth />
            <FormControl fullWidth>
              <InputLabel>Degree</InputLabel>
              <Select name="degree" value={formData.degree} onChange={handleInputChange} label="Degree">
                <MenuItem value="BS">Bacholor of Science</MenuItem>
                <MenuItem value="MS">Master of Science</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Graduation Year</InputLabel>
              <Select name="year" value={formData.year} onChange={handleInputChange} label="Graduation Year">
                {years.map((year) => (
                  <MenuItem key={year} value={year}>
                    {year}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Graduation Month</InputLabel>
              <Select
                name="graduation_month"
                value={formData.graduation_month}
                onChange={handleInputChange}
                label="Graduation Month"
              >
                {months.map((month) => (
                  <MenuItem key={month} value={month}>
                    {month}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Stack>
        )}

        {formData.role === 'alumni' && (
          <TextField
            name="company_name"
            label="Company Name"
            value={formData.company_name}
            onChange={handleInputChange}
            fullWidth
          />
        )}
      </Stack>

      <Stack alignItems="center" sx={{ my: 2 }}>
        <Link
          variant="subtitle2"
          underline="hover"
          onClick={() => {
            navigate('/login');
          }}
        >
          Sign in here
        </Link>
      </Stack>

      <LoadingButton
        fullWidth
        size="large"
        type="submit"
        variant="contained"
        onClick={() => {
          handleSubmit();
          console.log(formData);
        }}
      >
        Signup
      </LoadingButton>
      <Stack alignItems="center" sx={{ my: 2 }}>
        {errorMessage && (
          <Alert size="large" sx={{ whiteSpace: 'pre-line' }} severity="error">
            {errorMessage}
          </Alert>
        )}
        {successMessage && <Alert size="large"> {successMessage} </Alert>}
      </Stack>
    </>
  );
}
