import { Navigate, useRoutes } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Cookies from 'universal-cookie'
// layouts
import DashboardLayout from './layouts/dashboard';
import SimpleLayout from './layouts/simple';
//
import BlogPage from './pages/ApplicationPage';
import UserPage from './pages/UserPage';
import LoginPage from './pages/LoginPage';
import Page404 from './pages/Page404';
import ProductsPage from './pages/ProductsPage';
import DashboardAppPage from './pages/DashboardAppPage';
import DetailedJobPostPage from './pages/DetailedJobPostPage';
import SignupPage from './pages/SignupPage';
import SubmitApplicationPage from './pages/SubmitApplicationPage'
import EditApplicationPage from './pages/EditApplicationPage';
import NewJobPage from './pages/NewJobPage'
import ProfilePage from './pages/ProfilePage';
import DecideApplicationPage from './pages/DecideApplicationPage';
import DetailedViewApplicationPage from './pages/DetailedViewApplicationPage'
import MyJobPosts from './pages/MyJobPost';
import EditJobPostPage from './pages/EditJobPostPage'
import FavoriteJobPostPage from './pages/FavoriteJobPostPage';
import LeaderBoardPage from './pages/LeaderBoardPage';

// ----------------------------------------------------------------------

export default function Router() {
  const cookies = new Cookies();
  const authToken = cookies.get('token');
  const token = authToken?.split(' ')[1]; // Access the token here
  const [role, setRole] = useState(); 

  useEffect(() => {
    fetch(`/api/token?token=${token}`, {
      method: 'GET',
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data.student_id) {
          setRole('student');
        }
        else if(data.alumni_id){
          setRole('alumni');
          console.log(role);
        }
      })
      .catch((error) => {
        throw new Error(error);
      });
  });
  const routes = useRoutes([
    {
      path: '/',
      element: <DashboardLayout />,
      children: [
        { element: <Navigate to="/job-posts" />, index: true },
        { path: 'job-posts', element: <DashboardAppPage /> },
        { path: 'leaderboard', element: <LeaderBoardPage /> },
        { path: 'job-posts/:jobId', element: <DetailedJobPostPage role={role}/>},
        { path: 'edit-job-posts/:jobId', element: <EditJobPostPage />},
        { path: 'application/:jobId', element: <SubmitApplicationPage />},
        { path: 'edit-application/:applicationId', element: <EditApplicationPage />},
        { path: 'view-application/:applicationId', element: <DetailedViewApplicationPage/>},
        { path: 'new-job-posts', element: <NewJobPage /> },
        { path: 'user', element: <UserPage /> },
        { path: 'products', element: <ProductsPage /> },
        { path: 'profile', element: <ProfilePage /> },
        { path: 'application', element: (role === 'student' ? <BlogPage authToken={authToken}/> : <DecideApplicationPage authToken={authToken}/>) },
        { path: 'my-job-posts', element: (role === 'alumni' ? <MyJobPosts authToken={authToken}/> : <Page404/>) },
        { path: 'favorite-job-posts', element: (role === 'student' ? <FavoriteJobPostPage authToken={authToken}/> : <Page404/>) },
      ],
    },
    {
      path: 'login',
      element: <LoginPage />,
    },
    {
      path: 'signup',
      element: <SignupPage />,
    },
    {
      element: <SimpleLayout />,
      children: [
        { element: <Navigate to="/" />, index: true },
        { path: '404', element: <Page404 /> },
        { path: '*', element: <Navigate to="/404" /> },
      ],
    },
    {
      path: '*',
      element: <Navigate to="/404" />,
    },
  ]);

  return routes;
}
