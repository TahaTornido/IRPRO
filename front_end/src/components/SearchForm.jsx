import React, { useState, useEffect } from 'react';
import { Container, TextField, Button, Radio, RadioGroup, FormControlLabel, Checkbox, FormControl, FormLabel, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, CssBaseline, Grid } from '@mui/material';
import axios from 'axios';
import { useQuery, useMutation } from 'react-query';

// API call to fetch suggestions
// API call to fetch suggestions
// API call to fetch suggestions
const fetchSuggestions = async (query) => {
    const response = await fetch('http://127.0.0.1:5000/suggest_query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Assuming the response is an array of suggestions
  };
  
  // API call to correct query
  const correctQuery = async (query) => {
    const response = await fetch('http://127.0.0.1:5000/correct_query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  };
  
  // API call to perform search
  const searchAPI = async (searchData) => {
    const response = await fetch('http://127.0.0.1:5000/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(searchData),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  };
  
  // debounce function to delay the API call
  const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      timeoutId = setTimeout(() => {
        func(...args);
      }, delay);
    };
  };
export const SearchForm = () => {
   const [selectedOption, setSelectedOption] = useState('');
  const [useCluster, setUseCluster] = useState(false);
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [correctedQueries, setCorrectedQueries] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [isCorrecting, setIsCorrecting] = useState(false);

  const handleRadioChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleCheckboxChange = (event) => {
    setUseCluster(event.target.checked);
  };

  const handleInputChange = async (event) => {
    const newQuery = event.target.value;
    setQuery(newQuery);
    if (newQuery.length >= 3) {
      setIsCorrecting(true);
      try {
        const correctedData = await correctQuery(newQuery);
        setCorrectedQueries([correctedData.corrected_text]);
        fetchSuggestionsDebounced(correctedData.corrected_text);
      } catch (error) {
        console.error('Error correcting query:', error);
      } finally {
        setIsCorrecting(false);
      }
    } else {
      setSuggestions([]);
      setCorrectedQueries([]);
    }
  };

  const handleSearch = () => {
    mutation.mutate({
      query,
      dataset_name: selectedOption,
      is_cluster: useCluster ? 'yes' : 'no'
    });
  };

  const fetchSuggestionsDebounced = debounce(async (query) => {
    try {
      const data = await fetchSuggestions(query);
      setSuggestions(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      setSuggestions([]);
    }
  }, 300);

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    setSuggestions([]);
    setCorrectedQueries([]);
  };

  const handleCorrectedQueryClick = (correctedQuery) => {
    setQuery(correctedQuery);
    setSuggestions([]);
    setCorrectedQueries([]);
  };

  const mutation = useMutation(searchAPI, {
    onSuccess: (data) => {
      setSearchResults(Array.isArray(data) ? data : []);
    },
    onError: (error) => {
      console.error('Error:', error);
      setSearchResults([]);
    },
  });
  return (
    <Container>
      <CssBaseline />
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <TextField
            label="Search"
            variant="outlined"
            value={query}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
            disabled={isCorrecting}
          />
          <FormControl component="fieldset" margin="normal">
            <FormLabel component="legend">Search Options</FormLabel>
            <RadioGroup
              value={selectedOption}
              onChange={handleRadioChange}
            >
              <FormControlLabel value="lotte" control={<Radio />} label="Lotte" />
              <FormControlLabel value="qoura" control={<Radio />} label="Qoura" />
            </RadioGroup>
          </FormControl>
          <FormControlLabel
            control={<Checkbox checked={useCluster} onChange={handleCheckboxChange} />}
            label="Use Cluster"
          />
          <Button variant="contained" color="primary" onClick={handleSearch} disabled={mutation.isLoading || isCorrecting}>
            Search
          </Button>
          {mutation.isLoading && <p>Loading...</p>}
          {mutation.isError && <p>Error occurred: {mutation.error.message}</p>}
          {mutation.isSuccess && <p>Search completed successfully</p>}
        </Grid>
        <Grid item xs={12} md={6}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Suggestions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {suggestions.length > 0 ? (
                  suggestions.map((suggestion, index) => (
                    <TableRow key={index} onClick={() => handleSuggestionClick(suggestion)} style={{ cursor: 'pointer' }}>
                      <TableCell>{suggestion}</TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell>No suggestions available</TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
          <TableContainer component={Paper} style={{ marginTop: '20px' }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Corrected Queries</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {correctedQueries.length > 0 ? (
                  correctedQueries.map((correctedQuery, index) => (
                    <TableRow key={index} onClick={() => handleCorrectedQueryClick(correctedQuery)} style={{ cursor: 'pointer' }}>
                      <TableCell>{correctedQuery}</TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell>No corrected queries available</TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>
      </Grid>
      <TableContainer component={Paper} style={{ marginTop: '20px' }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Document Number</TableCell>
              <TableCell>Rank</TableCell>
              <TableCell>Normalized Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {searchResults.length > 0 ? (
              searchResults.map((result, index) => (
                <TableRow key={index}>
                  <TableCell>{result.docno}</TableCell>
                  <TableCell>{result.rank}</TableCell>
                  <TableCell>{result.normalized_score}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3}>
                  <Typography align="center">No results found</Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
  };
  export default SearchForm;
