import * as React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { Transaction } from './types';


// TODO: change on_menu_change type to the proper function!!!
export default function BasicMenu({options, initial_title, on_menu_change}: {options: string[], initial_title: string, on_menu_change: any}) {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [menuText, setMenuText] = React.useState(initial_title)
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = (value: string) => {
    if (typeof value === 'string') {
        setMenuText(value)
        on_menu_change(value)
    }
    // if (value) {
    //     setMenuText(value)
    // } else {
    //     setMenuText(menuText)
    // }
    // console.log(value)
    setAnchorEl(null);
  };

  const menu_list_options = options.map((option_item, index) => <MenuItem id={option_item} key={index} onClick={() => handleClose(option_item)}>{option_item}</MenuItem>);

  return (
    <div>
      <Button
        sx={{
          color: 'white',
          borderWidth: '2px',
          borderColor: '#fea028',
          '&:hover': {
            textDecoration: 'underline'
          } 
        }}
        id="basic-button"
        aria-controls={open ? 'basic-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
      >
        {menuText}
      </Button>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
      >
        {menu_list_options}
      </Menu>
    </div>
  );
}
