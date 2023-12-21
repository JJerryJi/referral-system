import { Helmet } from 'react-helmet-async';
import { sentenceCase } from 'change-case';
import { filter } from 'lodash';
import Cookies from 'universal-cookie';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

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
import { UserListHead, UserListToolbar } from '../sections/@dashboard/user';
import { fDateTime } from '../utils/formatTime';

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: 'job_id', label: 'Job Link', alignRight: false },
  { id: 'job_company', label: 'Job Company', alignRight: false },
  { id: 'job_open_status', label: 'Job Status', alignRight: false },
  { id: 'job_review_status', label: 'Review Status', alignRight: false },
  { id: 'num_of_applicants', label: 'Num of Applicants', alignRight: false },
  { id: 'detail_view', label: 'Action', alignRight: false },
];

// ----------------------------------------------------------------------

export default function MyJobPosts({ authToken }) {
  const token = authToken;
  console.log(token);
  const navigate = useNavigate();

  // multiple page design
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const [jobPosts, setJobPosts] = useState([]);
  const [order, setOrder] = useState('asc');
  const [orderBy, setOrderBy] = useState('job_id');
  const [filterName, setFilterName] = useState('');

  function descendingComparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
      return -1;
    }
    if (b[orderBy] > a[orderBy]) {
      return 1;
    }
    return 0;
  }

  function getComparator(order, orderBy) {
    return order === 'desc'
      ? (a, b) => descendingComparator(a, b, orderBy)
      : (a, b) => -descendingComparator(a, b, orderBy);
  }

  const handleFilterByName = (event) => {
    setFilterName(event.target.value);
  };

  function applySortFilter(array, comparator, query) {
    // console.log('app test');
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) return order;
      return a[1] - b[1];
    });
    if (query) {
      // console.log(array);
      query = query.toLowerCase();
      return filter(
        array,
        (el) =>
          el.job_id.toString().toLowerCase().includes(query) ||
          el.job_company.toString().toLowerCase().includes(query) ||
          el.job_open_status.toString().toLowerCase().includes(query) ||
          el.num_of_applicants.toString().toLowerCase().includes(query) ||
          el.job_review_status.toString().toLowerCase().includes(query)
      );
    }
    return stabilizedThis.map((el) => el[0]);
  }

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setPage(0);
    setRowsPerPage(parseInt(event.target.value, 10));
  };

  let filteredJobPosts = applySortFilter(jobPosts, getComparator(order, orderBy), filterName);

  const isNotFound = !filteredJobPosts.length && !!filterName;
  const jobPostsEndpoint = `http://127.0.0.1:8000/job/api/my_posts`;

  useEffect(() => {
    // Fetch applications with authorization header
    async function fetchApplications() {
      try {
        const response = await fetch(jobPostsEndpoint, {
          headers: {
            Authorization: token,
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setJobPosts(data.job_post);
        console.log(data.job_post);
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    }
    fetchApplications();
    filteredJobPosts = applySortFilter(jobPosts, getComparator(order, orderBy), '');
  }, []);

  return (
    <>
      <Helmet>
        <title> User | Referral_Finder </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            My Job Posts
          </Typography>
        </Stack>

        <Card>
          <UserListToolbar filterName={filterName} onFilterName={handleFilterByName} placeholderText={'Search...'} />
          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>
              <Table>
                <UserListHead
                  order={order}
                  orderBy={orderBy}
                  headLabel={TABLE_HEAD}
                  rowCount={jobPosts?.length}
                  onRequestSort={handleRequestSort}
                />
                <TableBody>
                  {filteredJobPosts.slice(rowsPerPage * page, rowsPerPage * page + rowsPerPage).map((jobPost) => {
                    /* eslint-disable  */
                    // console.log(application);
                    let { job_id, job_company, job_open_status, job_review_status, num_of_applicants } = jobPost;
                    /* eslint-disable  */
                    return (
                      <TableRow hover key={job_id} tabIndex={-1}>
                        <TableCell align="left">
                          <Button
                            onClick={() => {
                              navigate(`/job-posts/${job_id}`);
                            }}
                          >
                            Job {job_id}
                          </Button>
                        </TableCell>

                        <TableCell component="th" scope="row" padding="none">
                          <Stack direction="row" alignItems="center" spacing={2} sx={{ ml: '25%' }}>
                            <Typography variant="subtitle2" noWrap>
                              {job_company}
                            </Typography>
                          </Stack>
                        </TableCell>

                        <TableCell align="left">
                          <Label
                            color={
                              (job_open_status === 'accept' && 'info') ||
                              (job_open_status === 'closed' && 'error') ||
                              'success'
                            }
                          >
                            {job_open_status}
                          </Label>
                        </TableCell>

                        <TableCell align="left">
                          <Label
                            color={
                              (job_review_status === 'In-review' && 'info') ||
                              (job_review_status === 'Fail' && 'error') ||
                              'success'
                            }
                          >
                            {job_review_status}
                          </Label>
                        </TableCell>

                        <TableCell component="th" scope="row" padding="none">
                          <Stack direction="row" alignItems="center" spacing={2} sx={{ ml: '25%' }}>
                            <Typography variant="subtitle2" noWrap>
                              {num_of_applicants}
                            </Typography>
                          </Stack>
                        </TableCell>

                        <TableCell align="left">
                          <Button
                            size="small"
                            color="info"
                            variant="contained"
                            onClick={() => {
                              navigate(`/edit-job-posts/${job_id}`);
                            }}
                            disabled={job_review_status === 'In-review'}
                          >
                            Modify Job Post
                          </Button>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>

                {isNotFound && (
                  <TableBody>
                    <TableRow>
                      <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                        <Paper
                          sx={{
                            textAlign: 'center',
                          }}
                        >
                          <Typography variant="h6" paragraph>
                            Not found
                          </Typography>

                          <Typography variant="body2">
                            No results found for &nbsp;
                            <strong>&quot;{filterName}&quot;</strong>.
                            <br /> Try checking for typos or using complete words.
                          </Typography>
                        </Paper>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                )}
              </Table>
            </TableContainer>
          </Scrollbar>

          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={filteredJobPosts?.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Card>
      </Container>
    </>
  );
}
