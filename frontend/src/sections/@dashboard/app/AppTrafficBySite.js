// @mui
import PropTypes from 'prop-types';
import {
  Box,
  Card,
  Paper,
  Typography,
  CardHeader,
  CardContent,
  Button,
  InputAdornment,
  OutlinedInput,
  TablePagination
} from '@mui/material';
import { styled, alpha } from '@mui/material/styles';

import { useNavigate } from 'react-router-dom';
import Iconify from '../../../components/iconify';
import Label from '../../../components/label/Label';
// utils

// import Button from 'src/theme/overrides/Button';

// ----------------------------------------------------------------------

const StyledSearch = styled(OutlinedInput)(({ theme }) => ({
  width: 240,
  transition: theme.transitions.create(['box-shadow', 'width'], {
    easing: theme.transitions.easing.easeInOut,
    duration: theme.transitions.duration.shorter,
  }),
  '&.Mui-focused': {
    width: 320,
    boxShadow: theme.customShadows.z8,
  },
  '& fieldset': {
    borderWidth: `1px !important`,
    borderColor: `${alpha(theme.palette.grey[500], 0.32)} !important`,
  },
}));

AppTrafficBySite.propTypes = {
  title: PropTypes.string,
  subheader: PropTypes.string,
  list: PropTypes.array.isRequired,
};

export default function AppTrafficBySite({ title, subheader, list, filterName, onRequestSearch, length, rowsPerPage, page, setPage, setRowsPerPage, ...other }) {
  const navigate = useNavigate();
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setPage(0);
    setRowsPerPage(parseInt(event.target.value, 10));
  };
  return (
    <Card {...other}>

      <CardContent>
        <StyledSearch
          value={filterName}
          onChange={onRequestSearch}
          placeholder="Search Job Name or Company..."
          startAdornment={
            <InputAdornment position="start">
              <Iconify icon="eva:search-fill" sx={{ color: 'text.disabled', width: 20, height: 20 }} />
            </InputAdornment>
          }
          sx={{ mb: 1 }}
        />
        <Box
          sx={{
            display: 'grid',
            gap: 2,
            gridTemplateColumns: 'repeat(2, 1fr)',
          }}
        >
          {list.map((job) => (
            <Paper key={job.job_id} variant="outlined" sx={{ py: 2.5, textAlign: 'center' }}>
              <Typography variant="h6">
                Job {job.job_id}: {job.job_company}
              </Typography>
              <Typography variant="body3" sx={{ color: 'text.secondary' }}>
                {' '}
                {job.job_name}{' '}
              </Typography>
              <Box>
                {' '}
                <Button
                  sx={{ color: '#1565c0' }}
                  onClick={() => {
                    navigate(`/job-posts/${job.job_id}`);
                  }}
                >
                  Learn more about this Job
                </Button>
              </Box>
            </Paper>
          ))}
        </Box>

        <TablePagination
                rowsPerPageOptions={[6, 12, 24]}
                component="div"
                count={length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
              />
      </CardContent>
    </Card>
  );
}
