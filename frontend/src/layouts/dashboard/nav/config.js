// component
import SvgColor from '../../../components/svg-color';

// ----------------------------------------------------------------------

const icon = (name) => <SvgColor src={`/assets/icons/navbar/${name}.svg`} sx={{ width: 1, height: 1 }} />;

const navConfig = [
  {
    title: 'Job Post Dashboard',
    path: '/job-posts',
    icon: icon('ic_job_post'),
  },
  {
    title: 'Job Post LeaderBoard',
    path: '/leaderboard',
    icon: icon('ic_leaderboard'),
  },
  {
    title: 'application',
    path: '/application',
    icon: icon('ic_application'),
  },
  {
    title: 'profile',
    path: '/profile',
    icon: icon('ic_profile'),
  },
  {
    title: 'login',
    path: '/login',
    icon: icon('ic_lock'),
  },
  {
    title: 'signup',
    path: '/signup',
    icon: icon('ic_lock'),
  },
];

const nagConfigStudent = [  
  {
    title: 'Job Post Dashboard',
    path: '/job-posts',
    icon: icon('ic_job_post'),
  },
  {
    title: 'Job Post LeaderBoard',
    path: '/leaderboard',
    icon: icon('ic_leaderboard'),
  },
  {
    title: 'application',
    path: '/application',
    icon: icon('ic_application'),
  },
  {
    title: 'Saved Job Posts',
    path: '/favorite-job-posts',
    icon: icon('ic_favorite'),
  },
  {
    title: 'profile',
    path: '/profile',
    icon: icon('ic_profile'),
  },
  {
    title: 'login',
    path: '/login',
    icon: icon('ic_lock'),
  },
  {
    title: 'signup',
    path: '/signup',
    icon: icon('ic_lock'),
  },
];

const nagConfigAlumni = [  
  {
    title: 'Job Posts Dashboard',
    path: '/job-posts',
    icon: icon('ic_job_post'),
  },
  {
    title: 'Post LeaderBoard',
    path: '/leaderboard',
    icon: icon('ic_leaderboard'),
  },
  {
    title: 'My Posts',
    path: '/my-job-posts',
    icon: icon('ic_application'),
  },
  {
    title: 'application',
    path: '/application',
    icon: icon('ic_application'),
  },
  {
    title: 'profile',
    path: '/profile',
    icon: icon('ic_profile'),
  },
  {
    title: 'login',
    path: '/login',
    icon: icon('ic_lock'),
  },
  {
    title: 'signup',
    path: '/signup',
    icon: icon('ic_lock'),
  },
];
export { navConfig, nagConfigStudent, nagConfigAlumni };
