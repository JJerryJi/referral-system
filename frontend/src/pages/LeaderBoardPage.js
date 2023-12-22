import { useEffect, useState } from 'react';

import { Grid, Container, Stack, Typography, TablePagination } from '@mui/material';
import { Helmet } from 'react-helmet-async';
import { AppNewsUpdate } from '../sections/@dashboard/app';

// ----------------------------------------------------------------------

export default function LeaderBoardPage() {
  const [leadingPosts, setLeadingPosts] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetch(`/job/api/leaderboard?page=${page}&per_page=${rowsPerPage}`)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        return null;
      })
      .then((data) => {
        if (data) {
          setTotal(data.total_num);
          // Extract job post objects from the numbered keys
          // Extract job post objects from the numbered keys while excluding "total_num"
          const jobPosts = Object.keys(data)
            .filter((key) => key !== 'total_num')
            .map((key) => data[key]);
          // Set the job posts in the state
          setLeadingPosts(jobPosts);
          console.log(jobPosts);
        } else {
          throw new Error('Invalid data');
        }
      })
      .catch((error) => {
        throw new Error(`Error Fetching the leaderboard information: ${error.message}`);
      });
  }, [page, rowsPerPage]);

  return (
    <>
      <Helmet>
        <title> LeaderBoard </title>
      </Helmet>

      <Container maxWidth="xl">
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={1}>
          <Typography variant="h4" color="#2196f3">
            Top Job LeaderBoard
          </Typography>
        </Stack>

        <Grid container spacing={3}>
          <Grid item xs={30} md={16} lg={16}>
            <AppNewsUpdate
              list={leadingPosts}
              total={total}
              rowsPerPage={rowsPerPage}
              page={page}
              setPage={setPage}
              setRowsPerPage={setRowsPerPage}
            />
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
