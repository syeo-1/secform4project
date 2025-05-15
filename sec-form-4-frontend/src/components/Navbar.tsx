// import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import { useEffect, useState } from "react"
// import SearchResults from './SearchResults';
import TextField from '@mui/material/TextField';
import { Autocomplete } from '@mui/material';
import { useNavigate } from 'react-router';

const BASE_URL = 'http://127.0.0.1:8000/api/'

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    [theme.breakpoints.up('sm')]: {
      width: '12ch',
      '&:focus': {
        width: '20ch',
      },
    },
  },
}));

export default function SearchAppBar() {

  const [search_results_api, set_search_results_api] = useState<string[]>([])
  const [highlightedOption, setHighlightedOption] = useState<string | null>("");
  const [inputValue, setInputValue] = useState("")
  const navigate = useNavigate()

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      event.preventDefault() // prevent a form submission
      if (highlightedOption) {
        navigate(`/info/${encodeURIComponent(highlightedOption)}`);
      }
    }
  }
  const handleLeftClick = () => {
    if (highlightedOption) {
      navigate(`/info/${encodeURIComponent(highlightedOption)}`);
    }
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="open drawer"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
          >
            InsiderInsight
          </Typography>
          <Autocomplete
            options={search_results_api}
            getOptionLabel={(option) => option}
            onInputChange={(_, newInputValue) => {
              fetch(`${BASE_URL}common/search/${newInputValue}`)
                .then((response) => response.json())
                .then((json) => { set_search_results_api(json)})
              setInputValue(newInputValue)
            }}
            onHighlightChange={(_, option) => {
              setHighlightedOption(option);
            }}
            sx={{ width: 300}}
            renderInput={(params: any) => <TextField {...params} label="Search" />}
            onKeyDown={handleKeyDown}
            onChange={handleLeftClick}
            />
        </Toolbar>
      </AppBar>
    </Box>
  );
}
