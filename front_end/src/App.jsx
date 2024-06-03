import { useState } from 'react'
import React from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { SearchForm } from './components/SearchForm'
import { CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
const theme = createTheme({
  palette: {
    mode: 'dark', // تأكد من استخدام الوضع الفاتح
  },
});

const queryClient = new QueryClient();

const App = () => {
  const [view, setView] = React.useState('search'); // 'search' or 'results'
  const [searchData, setSearchData] = React.useState(null);

  const handleSearch = (data) => {
    setSearchData(data);
    setView('results');
  };

  const handleBack = () => {
    setView('search');
  };

  return (
    // <ThemeProvider theme={theme}>
    //   <CssBaseline />
    //   <div>
    //     <h1>Search Application</h1>
    //     <SearchForm />
    //   </div>
    // </ThemeProvider>
    <QueryClientProvider client={queryClient}>
    <ThemeProvider theme={theme}>
    <CssBaseline />
    <div>
      <h1>Search Application</h1>
      {view === 'search' ? (
        <SearchForm onSearch={handleSearch} />
      ) : (
        <Results data={{ ...searchData, onBack: handleBack }} />
      )}
    </div>
  </ThemeProvider>
  </QueryClientProvider>
  );
};

export default App;
// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vitejs.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.jsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//       <Button variant="contained">Hello world</Button>
//     </>


//   )
// }

// export default App
