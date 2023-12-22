import PropTypes from 'prop-types';
import { set, sub } from 'date-fns';
import { noCase } from 'change-case';
import { faker } from '@faker-js/faker';
import { useState, useEffect } from 'react';
import Cookies from 'universal-cookie';
// @mui
import {
  Box,
  List,
  Badge,
  Button,
  Avatar,
  Tooltip,
  Divider,
  Popover,
  Typography,
  IconButton,
  ListItemText,
  ListSubheader,
  ListItemAvatar,
  ListItemButton,
} from '@mui/material';

// utils
import { fToNow } from '../../../utils/formatTime';
// components
import Iconify from '../../../components/iconify';
import Scrollbar from '../../../components/scrollbar';

// ----------------------------------------------------------------------

export default function NotificationsPopover() {
  const token = new Cookies().get('token');
  const [notifications, setNotifications] = useState([]);
  const [totalUnRead, setTotalUnRead] = useState(0);
  const [displayNum, setDisplayNum] = useState(5);

  useEffect(() => {
    // manage websocket connection & ready to re-connect every 3 seconds
    const websocketConnect = (data) => {
      const newSocket = new WebSocket(`ws://127.0.0.1:8002/ws/${data.user_id}`);

      newSocket.addEventListener('open', () => {
        console.log('WebSocket connection opened');
      });

      newSocket.onmessage = (event) => {
        // Handle incoming WebSocket messages for the applicant
        const newNotification = JSON.parse(event.data);
        console.log('Received WebSocket message:', newNotification);
        if (newNotification.filteredId && newNotification.filteredId === data.user_id) {
          setNotifications((prevNotifications) => [newNotification, ...prevNotifications]);
          setTotalUnRead((num) => num + 1);
        }
      };

      newSocket.onclose = () => {
        setTimeout(websocketConnect, 5000, data);
        console.log('reconnected');
      };
    };

    // Fetch the user's ID using the token
    fetch(`http://127.0.0.1:8088/api/token?token=${token?.split(' ')[1]}`, {
      method: 'GET',
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
        // call websocket connection here:
        websocketConnect(data);
      })
      .catch((error) => {
        throw new Error(error);
      });
  }, [token]);

  const [open, setOpen] = useState(null);

  const handleOpen = (event) => {
    setOpen(event.currentTarget);
  };

  const handleClose = () => {
    setOpen(null);
  };

  const handleMarkAllAsRead = () => {
    setNotifications(
      notifications.map((notification) => ({
        ...notification,
        isUnRead: false,
      }))
    );

    setTotalUnRead(0);
  };

  const handleMarkAsRead = (notificationId, readOrUnread) => {
    // Find the clicked notification by its ID
    const updatedNotifications = notifications.map((notification) => {
      if (notification.id === notificationId) {
        return {
          ...notification,
          isUnRead: !notification.isUnRead,
        };
      }
      return notification;
    });
    // Update the state with the modified notifications
    setNotifications(updatedNotifications);
    if (readOrUnread === 'read') {
      setTotalUnRead((num) => num - 1);
    } else {
      setTotalUnRead((num) => num + 1);
    }
  };

  return (
    <>
      <IconButton color={open ? 'primary' : 'default'} onClick={handleOpen} sx={{ width: 40, height: 40 }}>
        <Badge badgeContent={totalUnRead} color="error">
          <Iconify icon="eva:bell-fill" />
        </Badge>
      </IconButton>

      <Popover
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            mt: 1.5,
            ml: 0.75,
            width: 360,
          },
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', py: 2, px: 2.5 }}>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="subtitle1">Notifications</Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              You have {totalUnRead} unread messages
            </Typography>
          </Box>

          {totalUnRead > 0 && (
            <Tooltip title=" Mark all as read">
              <IconButton color="primary" onClick={handleMarkAllAsRead}>
                <Iconify icon="eva:done-all-fill" />
              </IconButton>
            </Tooltip>
          )}
        </Box>

        <Divider sx={{ borderStyle: 'dashed' }} />

        <Scrollbar sx={{ height: { xs: 340, sm: 'auto' } }}>
          <List
            disablePadding
            subheader={
              <ListSubheader disableSticky sx={{ py: 1, px: 2.5, typography: 'overline' }}>
                New
              </ListSubheader>
            }
          >
            {notifications
              .slice(0, displayNum)
              .map(
                (notification) =>
                  notification.isUnRead === true && (
                    <NotificationItem
                      key={notification.id}
                      notification={notification}
                      onClick={() => handleMarkAsRead(notification.id, 'read')}
                    />
                  )
              )}
          </List>

          <List
            disablePadding
            subheader={
              <ListSubheader disableSticky sx={{ py: 1, px: 2.5, typography: 'overline' }}>
                Before that
              </ListSubheader>
            }
          >
            {notifications
              .slice(0, displayNum)
              .map(
                (notification) =>
                  notification.isUnRead === false && (
                    <NotificationItem
                      key={notification.id}
                      notification={notification}
                      onClick={() => handleMarkAsRead(notification.id, 'unread')}
                    />
                  )
              )}
          </List>
        </Scrollbar>

        <Divider sx={{ borderStyle: 'dashed' }} />

        <Box sx={{ p: 1 }}>
          <Button fullWidth disableRipple onClick={()=>{setDisplayNum(notifications.length)}}>
            View All
          </Button>
        </Box>
      </Popover>
    </>
  );
}

// ----------------------------------------------------------------------

NotificationItem.propTypes = {
  notification: PropTypes.shape({
    // createdAt: PropTypes.instanceOf(Date),
    id: PropTypes.string,
    isUnRead: PropTypes.bool,
    title: PropTypes.string,
    description: PropTypes.string,
    type: PropTypes.string,
    avatar: PropTypes.any,
  }),
};

// Function to format the time elapsed since the notification was created
const formatTimeElapsed = (createdAt) => {
  const currentTime = new Date();
  const createdAtTime = new Date(createdAt);
  const timeDifference = currentTime - createdAtTime;
  const minutesDifference = Math.floor(timeDifference / (1000 * 60));

  if (minutesDifference < 1) {
    return 'less than one min ago';
  }

  if (minutesDifference < 60) {
    return `about ${minutesDifference} min ago`;
  }
  const hoursDifference = Math.floor(minutesDifference / 60);
  return `about ${hoursDifference} hr ago`;
};

function NotificationItem({ notification, onClick }) {
  const { avatar, title } = renderContent(notification);
  const [elapsedTime, setElapsedTime] = useState(formatTimeElapsed(notification.createdAt));

  // Update the elapsed time every minute
  useEffect(() => {
    const intervalId = setInterval(() => {
      setElapsedTime(formatTimeElapsed(notification.createdAt));
    }, 60000); // Update every minute (60000 milliseconds)

    // Clear the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, [notification.createdAt, elapsedTime]);

  return (
    <ListItemButton
      sx={{
        py: 1.5,
        px: 2.5,
        mt: '1px',
        ...(notification.isUnRead && {
          bgcolor: 'action.selected',
        }),
      }}
      onClick={onClick}
    >
      <ListItemAvatar>
        <Avatar sx={{ bgcolor: 'background.neutral' }}>{avatar}</Avatar>
      </ListItemAvatar>
      <ListItemText
        primary={title}
        secondary={
          <Typography
            variant="caption"
            sx={{
              mt: 0.5,
              display: 'flex',
              alignItems: 'center',
              color: 'text.disabled',
            }}
          >
            <Iconify icon="eva:clock-outline" sx={{ mr: 0.5, width: 16, height: 16 }} />
            {elapsedTime}
          </Typography>
        }
      />
    </ListItemButton>
  );
}

// ----------------------------------------------------------------------

function renderContent(notification) {
  const title = (
    <Typography variant="subtitle2">
      {notification.title}
      <Typography component="span" variant="body2" sx={{ color: 'text.secondary' }}>
        &nbsp; {noCase(notification.description)}
      </Typography>
    </Typography>
  );

  if (notification.type === 'order_placed') {
    return {
      avatar: <img alt={notification.title} src="/assets/icons/ic_notification_package.svg" />,
      title,
    };
  }
  if (notification.type === 'order_shipped') {
    return {
      avatar: <img alt={notification.title} src="/assets/icons/ic_notification_shipping.svg" />,
      title,
    };
  }
  if (notification.type === 'mail') {
    return {
      avatar: <img alt={notification.title} src="/assets/icons/ic_notification_mail.svg" />,
      title,
    };
  }
  if (notification.type === 'chat_message') {
    return {
      avatar: <img alt={notification.title} src="/assets/icons/ic_notification_chat.svg" />,
      title,
    };
  }
  return {
    avatar: notification.avatar ? <img alt={notification.title} src={notification.avatar} /> : null,
    title,
  };
}
