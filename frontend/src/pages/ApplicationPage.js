import { Helmet } from 'react-helmet-async';
import { sentenceCase } from 'change-case';
import { filter } from 'lodash';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// @mui
import {
  Card,
  Table,
  Stack,
  Paper,
  Button,
  TableRow,
  TableBody,
  TableCell,
  Container,
  Typography,
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
  { id: 'id', label: 'Application ID', alignRight: false },
  { id: 'job_id', label: 'Job Link', alignRight: false },
  { id: 'date', label: 'Applied Date', alignRight: false },
  { id: 'status', label: 'Status', alignRight: false },
  { id: 'action', label: 'Action', alignRight: false },
];

// ----------------------------------------------------------------------

export default function BlogPage({ authToken }) {
  const token = authToken;
  const navigate = useNavigate();

  // multiple page design
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const [applications, setApplications] = useState([]);
  const [order, setOrder] = useState('asc');
  const [orderBy, setOrderBy] = useState('id');
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

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setPage(0);
    setRowsPerPage(parseInt(event.target.value, 10));
  };

  function applySortFilter(array, comparator, query) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) return order;
      return a[1] - b[1];
    });
    if (query) {
      return filter(
        array,
        (el) =>
          el.id.toString().toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
          el.status.toString().toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
          el.job_id.toString().toLowerCase().indexOf(query.toLowerCase()) !== -1
      );
    }
    return stabilizedThis.map((el) => el[0]);
  }

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };
  let filteredApplication = applySortFilter(applications, getComparator(order, orderBy), filterName);

  const isNotFound = !filteredApplication.length && !!filterName;
  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - applications.length) : 0;
  const ApplicationEndpoint = `http://127.0.0.1:8000/application/api/application`;

  useEffect(() => {
    // Fetch applications with authorization header
    async function fetchApplications() {
      try {
        const response = await fetch(ApplicationEndpoint, {
          headers: {
            Authorization: token,
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setApplications(data.application);
        // console.log(data.application);
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    }
    fetchApplications();
    filteredApplication = applySortFilter(applications, getComparator(order, orderBy), '');
  }, []);

  return (
    <>
      <Helmet>
        <title> User | Referral_Finder </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            My Applications
          </Typography>
        </Stack>

        <Card>
          <UserListToolbar filterName={filterName} onFilterName={handleFilterByName} placeholderText={'Search ...'} />
          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>
              <Table>
                <UserListHead
                  order={order}
                  orderBy={orderBy}
                  headLabel={TABLE_HEAD}
                  rowCount={applications?.length}
                  onRequestSort={handleRequestSort}
                />
                <TableBody>
                  {filteredApplication
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((application) => {
                      /* eslint-disable  */
                      // console.log(application);
                      let { id, job_id, modified_date, status } = application;
                      /* eslint-disable  */
                      return (
                        <TableRow hover key={id} tabIndex={-1}>
                          <TableCell component="th" scope="row" padding="none">
                            <Stack direction="row" alignItems="center" spacing={2} sx={{ ml: '25%' }}>
                              <Typography variant="subtitle2" noWrap>
                                {id}
                              </Typography>
                            </Stack>
                          </TableCell>

                          <TableCell align="left">
                            <Button
                              onClick={() => {
                                navigate(`/job-posts/${job_id}`);
                              }}
                            >
                              Job {job_id}
                            </Button>
                          </TableCell>

                          <TableCell align="left">
                            {fDateTime(modified_date)} {/* Make sure to format the date as needed */}
                          </TableCell>

                          <TableCell align="left">
                            <Label
                              color={
                                (status === 'In Progress' && 'info') ||
                                (status === 'Not-moving-forward' && 'error') ||
                                'success'
                              }
                            >
                              {sentenceCase(status)}
                            </Label>
                          </TableCell>

                          <TableCell align="left">
                            {status === 'In Progress' && (
                              <Button
                                size="small"
                                color="info"
                                variant="contained"
                                onClick={() => {
                                  navigate(`/edit-application/${id}`);
                                }}
                              >
                                Modify Application
                              </Button>
                            )}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  {emptyRows > 0 && (
                    <TableRow style={{ height: 53 * emptyRows }}>
                      <TableCell colSpan={6} />
                    </TableRow>
                  )}
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
            count={filteredApplication?.length}
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
