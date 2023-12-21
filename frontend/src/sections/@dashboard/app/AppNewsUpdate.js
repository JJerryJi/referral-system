import { useNavigate } from 'react-router-dom';

// @mui
import PropTypes from 'prop-types';
import { Box, Stack, Link, Card, Button, Divider, Typography, CardHeader, TablePagination } from '@mui/material';
// utils
import { fToNow } from '../../../utils/formatTime';
// components
import Iconify from '../../../components/iconify';
import Scrollbar from '../../../components/scrollbar';

// ----------------------------------------------------------------------

AppNewsUpdate.propTypes = {
  title: PropTypes.string,
  subheader: PropTypes.string,
  list: PropTypes.array.isRequired,
};

export default function AppNewsUpdate({
  // title & subheader
  title,
  subheader,
  // list of leading job posts
  list,
  // total number of job posts
  total,
  // callback functions
  rowsPerPage,
  setRowsPerPage,
  page,
  setPage,
  ...other
}) {
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
    console.log(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setPage(0);
    setRowsPerPage(parseInt(event.target.value, 10));
  };

  return (
    <Card {...other}>
      <CardHeader title={title} subheader={subheader} />

      <Scrollbar>
        <Stack spacing={3} sx={{ p: 3, pr: 0 }}>
          {list.map((news, index) => (
            <NewsItem key={index + page * rowsPerPage} news={news} id={index + page * rowsPerPage} />
          ))}
        </Stack>
      </Scrollbar>

      <Divider />

      <TablePagination
        rowsPerPageOptions={[5, 10, 20]}
        component="div"
        count={total}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />

      {/* <Box sx={{ p: 2, textAlign: 'right' }}>
        <Button size="small" color="inherit" endIcon={<Iconify icon={'eva:arrow-ios-forward-fill'} />}>
          View all
        </Button>
      </Box> */}
    </Card>
  );
}

// ----------------------------------------------------------------------

NewsItem.propTypes = {
  news: PropTypes.shape({
    description: PropTypes.string,
    image: PropTypes.string,
    postedAt: PropTypes.instanceOf(Date),
    title: PropTypes.string,
  }),
};

/* eslint-disable */
function NewsItem({ id, news }) {
  const navigate = useNavigate();
  const { job_post_id, job_name, job_company, created_time, score } = news;
  return (
    <Stack direction="row" alignItems="center" spacing={2}>
      <Box
        component="img"
        alt={`${id + 1}`}
        src={`/assets/icons/leaderboard/${id + 1}.svg`}
        sx={{ width: 48, height: 48, borderRadius: 1.5, flexShrink: 0 }}
      />
      <Box sx={{ minWidth: 240, flexGrow: 1 }}>
        <Link
          color="inherit"
          variant="subtitle2"
          underline="hover"
          noWrap
          onClick={() => navigate(`/job-posts/${job_post_id}`)}
        >
          {job_name}
        </Link>

        <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
          {job_company}
        </Typography>
      </Box>

      <Box sx={{textAlign:'right'}}>
        <Typography variant="body2" sx={{ pr: 3, flexShrink: 0, color: 'text.primary' }}>
          {score} points
        </Typography>
        <Typography variant="caption" sx={{ pr: 3, flexShrink: 0, color: 'text.secondary' }}>
          {fToNow(created_time)}
        </Typography>
      </Box>
    </Stack>
  );
}
/* eslint-disable */
