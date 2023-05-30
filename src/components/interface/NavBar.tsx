import { Avatar } from '@mui/material/index';
import { useState } from 'react'

import classes from '#/Styles/NavBar.module.css'


export function UserIcon({ username, avatar }) {
  // const classes = useStyles();
  const [usernameVisible, setUsernameVisible] = useState(false);

  const handleMouseEnter = () => {
    setUsernameVisible(true);
  };

  const handleMouseLeave = () => {
    setUsernameVisible(false);
  };

  return (
    <div className={classes.root} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
      <div className={usernameVisible ? classes.usernameVisible : classes.username}>{username}</div>
      <Avatar src={avatar} alt={username} />
    </div>
  );
}
