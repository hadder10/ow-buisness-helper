import React, { useState } from "react";
import "./App.css";
import { Button, Stack, IconButton, Paper, Typography } from "@mui/material";
import TextField from "@mui/material/TextField";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { deepPurple } from "@mui/material/colors";

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [inputText, setInputText] = useState("");

  const theme = createTheme({
    palette: {
      mode: darkMode ? "dark" : "light",
      primary: {
        main: deepPurple[500],
        light: deepPurple[300],
        dark: deepPurple[700],
      },
      background: {
        default: darkMode ? "#121212" : "#fff",
        paper: darkMode ? deepPurple[900] : deepPurple[50],
      },
    },
  });

  React.useEffect(() => {
    document.body.style.backgroundColor = darkMode ? "#121212" : "#fff";
    document.body.style.color = darkMode ? "#fff" : "#121212";
  }, [darkMode]);

  return (
    <ThemeProvider theme={theme}>
      <div
        className="dynamic-background"
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: darkMode
            ? `linear-gradient(-45deg, 
          ${deepPurple[900]} 0%, 
          #121212 25%, 
          ${deepPurple[800]} 51%, 
          #121212 100%)`
            : `linear-gradient(-45deg, 
          ${deepPurple[50]} 0%, 
          #ffffff 25%, 
          ${deepPurple[100]} 51%, 
          #ffffff 100%)`,
        }}
      >
        <IconButton
          sx={{
            position: "fixed",
            top: 16,
            right: 16,
            zIndex: 1000,
          }}
          onClick={() => setDarkMode((prev) => !prev)}
          color="inherit"
        >
          {darkMode ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>
        <Stack
          spacing={4}
          sx={{
            height: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Typography
            variant="h2"
            component="h1"
            color="primary"
            sx={{
              mb: 4,
              fontWeight: 500,
              textAlign: "center",
              fontFamily: '"GOST Type B", serif',
            }}
          >
            Введите артикул с Wildberries
          </Typography>

          <Stack
            direction="row"
            spacing={2}
            sx={{
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <TextField
              id="filled-basic"
              label="Введите текст"
              variant="filled"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              sx={{
                width: "600px",
                // minWidth: '300px', // минимальная ширина
                // width: '30%',
              }}
            />
            <Button
              variant="contained"
              color="primary"
              disableRipple
              disableElevation
              sx={{ minWidth: "200 px", minHeight: "56px" }}
            >
              Получить рекомендации
            </Button>
          </Stack>

          {inputText && (
            <Paper
              elevation={3}
              sx={{
                p: 2,
                width: "40%",
                bgcolor: darkMode
                  ? "rgba(103, 58, 183, 0.15)"
                  : "rgba(103, 58, 183, 0.05)",
                borderRadius: 1,
                transition: "all 0.3s ease",
              }}
            >
              Артикул {inputText} не найден
            </Paper>
          )}
        </Stack>
      </div>
    </ThemeProvider>
  );
}

export default App;
