import * as React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { Transaction } from './types';



export default function BasicMenu({options, update_data, initial_title}: {options: string[], update_data: React.Dispatch<React.SetStateAction<Transaction[]>>, initial_title: string}) {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [menuText, setMenuText] = React.useState(initial_title)
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = (value: string) => {
    if (typeof value === 'string') {
        setMenuText(value)
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
