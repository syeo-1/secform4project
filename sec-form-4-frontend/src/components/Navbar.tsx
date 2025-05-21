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
import { SvgIcon } from '@mui/material';
import logo from './insiderinsight_logo.svg'
// import { ReactComponent as Logo } from './insiderinsight_logo.svg';
import Paper from '@mui/material/Paper';


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

// const customPaper = (props: any) => {
//     return <Paper elevation={7} {...props} />;
// }

export default function SearchAppBar() {

  const [search_results_api, set_search_results_api] = useState<string[]>([])
  const [search_results_initial, set_search_results_initial] = useState<string[]>([])
  const [highlightedOption, setHighlightedOption] = useState<string | null>("");
  const [inputValue, setInputValue] = useState("")
  const [search_label, set_search_label] = useState("Search")
  const navigate = useNavigate()
  
  useEffect((() => {
    fetch(`${BASE_URL}common/search/`)
      .then((response) => response.json())
      .then((json) => { set_search_results_initial(json)})
    }
  ), [])

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
  
  const goHome = () => {
    navigate('/')
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar sx={{backgroundColor: 'black'}} position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="open drawer"
            sx={{ mr: 2 }}
            onClick={goHome}
          >
            {/* <MenuIcon /> */}
           <img src={logo} alt="icon" width={40} height={30} /> 
          </IconButton>
          <Typography
            // variant="h6"
            noWrap
            component="div"
            sx={{ display: { xs: 'none', sm: 'block' },
            paddingRight: '65vw'
          }}
          >
            <h2 onClick={goHome} style={{cursor: 'pointer'}}>InsiderInsight</h2>
          </Typography>

          <Autocomplete
          // TODO: handle the notch on the autocomplete search bar top left!!!!
            slotProps={{
              paper: {
                sx: {
                  backgroundColor: 'black',
                  color: 'white',
                  '& .MuiAutocomplete-option': {
                    backgroundColor: 'black',
                    color: 'white',
                    '&[aria-selected="true"]': {
                      backgroundColor: 'white',
                      color: 'black',
                    },
                    // '&:hover': {
                    //   backgroundColor: '#282a35',
                    // },
                  },
                },
              },
            }}
            options={search_results_api}
            noOptionsText=""
            getOptionLabel={(option) => option}
            onInputChange={(_, newInputValue) => {
              set_search_results_api(search_results_initial.filter(s => s.toLowerCase().includes(newInputValue.toLowerCase())))
              setInputValue(newInputValue)
            }}
            onOpen={() => {
              set_search_label("")
            }}
            onHighlightChange={(_, option) => {
              setHighlightedOption(option);
            }}
            sx={{ width: 300,
              backgroundColor: 'black', 
              borderRadius: '10px', 
              "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {borderColor: "black"},
              '& .MuiOutlinedInput-root': {
              '& .MuiOutlinedInput-notchedOutline': {
                borderColor: 'dodgerblue', // default border
                // borderWidth: '2px',
              },
              '&:hover .MuiOutlinedInput-notchedOutline': {
                borderColor: 'dodgerblue', // hover effect
              },
              '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                borderColor: 'dodgerblue', // focus effect
              },
              input: {
                color: 'white'
              }
            }}}
            renderInput={(params: any) => <TextField 
              {...params} 
              label="" 
              placeholder="Search" not/>}
            onKeyDown={handleKeyDown}
            onChange={handleLeftClick}
            // slotProps={{
            //   popper: {
            //     sx: {
            //       '& .MuiAutocomplete-paper': {
            //         backgroundColor: 'black',
            //         color: 'white',
            //       },
            //       '& .MuiAutocomplete-option': {
            //         backgroundColor: 'black',
            //         color: 'white',
            //         '&[aria-selected="true"]': {
            //           backgroundColor: 'white',
            //         },
            //         '&:hover': {
            //           backgroundColor: '#282a35',
            //         },
            //       },
            //     },
            //   },
            // }}
            />
        </Toolbar>
      </AppBar>
    </Box>
  );
}
