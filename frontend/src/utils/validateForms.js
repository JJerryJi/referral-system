export function validateJobPostForm(formData) {
  const errors = {};

  // Validate job_name
  const jobNameValidator = /^[a-zA-Z0-9\s-@_()]{10,50}$/;
  if (!formData.job_name.trim()) {
    errors.job_name = 'Job Name is required';
  } else if (!jobNameValidator.test(formData.job_name)) {
    errors.job_name =
      'Job Name should be 10-50 characters long and may only contain letters, numbers, spaces, and hyphens.';
  }

  // Validate job_company
  const jobCompanyValidator = /^[a-zA-Z0-9\s\-()_[\]!@]{3,64}$/;
  if (!formData.job_company.trim()) {
    errors.job_company = 'Company Name is required';
  } else if (!jobCompanyValidator.test(formData.job_company)) {
    errors.job_company =
      'Company Name should be 3-40 characters, including letters, numbers, spaces, and some special symbols';
  }

  if (!formData.job_requirement.trim()) {
    errors.job_requirement = 'Job Requirement is required';
  } else if (formData.job_requirement.trim().length < 10 || formData.job_requirement.trim().length > 1000) {
    errors.job_requirement = 'Job Requirement should be between 10 and 1000 characters.';
  }

  // Validate question
  if (!formData.job_question.trim()) {
    errors.job_question = 'Job Question is required';
  }

  if (!formData.job_description.trim()) {
    errors.job_description = 'Job Description is required';
  } else if (formData.job_description.trim().length < 10 || formData.job_description.trim().length > 1000) {
    errors.job_description = 'Job Description should be between 10 and 1000 characters.';
  }
  // console.log(errors);
  return errors;
}

export const validateSignUpForm = (formData) => {
  const errors = {};

  // Define required fields for each role
  const requiredFields = {
    common: ['username', 'password', 'location', 'email', 'first_name', 'last_name', 'role'],
    student: ['school', 'year_in_school', 'major', 'degree', 'year', 'graduation_month'],
    alumni: ['company_name'],
  };

  const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
  const usernameRegex = /^[A-Za-z0-9_]{3,15}$/; // Fixed the regex
  const firstNameRegex = /^[A-Za-z]{2,20}$/; // Fixed the regex
  const lastNameRegex = /^[A-Za-z]{2,20}$/; // Fixed the regex

  // Check common fields
  requiredFields.common.forEach((field) => {
    if (!formData[field]) {
      errors[field] = `Missing required field: ${field}`;
    } else if (field === 'email' && !formData[field].match(emailRegex)) {
      errors[field] = 'Invalid email address';
    } else if (field === 'username' && !formData[field].match(usernameRegex)) {
      errors[field] = 'Invalid username. It should consist 3 - 15 chars or numbers.';
    } else if (field === 'first_name' && !formData[field].match(firstNameRegex)) {
      errors[field] = 'Invalid first_name. It should consist 2 - 20 chars.';
    } else if (field === 'last_name' && !formData[field].match(lastNameRegex)) {
      errors[field] = 'Invalid last_name. It should consist 2 - 20 chars';
    }
  });

  // Check role-specific fields
  if (formData.role === 'student' || formData.role === 'alumni') {
    requiredFields[formData.role].forEach((field) => {
      if (!formData[field]) {
        errors[field] = `Missing required field: ${field}`;
      }
    });
  }

  return errors;
};
