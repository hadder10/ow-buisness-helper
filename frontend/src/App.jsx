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
  const [inputText2, setInputText2] = useState("");
  const [productData, setProductData] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

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

  const fetchProductInfo = async (articul) => {
    try {
      const productResponse = await fetch(
        `http://localhost:5000/api/product/${articul}`
      );
      if (!productResponse.ok) {
        throw new Error("Product data fetch failed");
      }
      const productData = await productResponse.json();
      setProductData(productData);
    } catch (error) {
      console.error("Error fetching product info:", error);
      setProductData(null);
    }
  };

  const fetchProductData = async (articul) => {
    try {
      setIsLoading(true);

      const downloadResponse = await fetch(
        `http://localhost:5000/api/download/${articul}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ search_query: inputText2 }),
        }
      );

      if (!downloadResponse.ok) {
        throw new Error("Download failed");
      }

      await downloadResponse.json();

      const productResponse = await fetch(
        `http://localhost:5000/api/product/${articul}`
      );
      if (!productResponse.ok) {
        throw new Error("Product data fetch failed");
      }
      const productData = await productResponse.json();
      setProductData(productData);

      const recommendationsResponse = await fetch(
        `http://localhost:5000/api/recommendations/${articul}`
      );
      if (!recommendationsResponse.ok) {
        throw new Error("Recommendations fetch failed");
      }
      const recommendationsData = await recommendationsResponse.json();
      setRecommendations(recommendationsData);
    } catch (error) {
      console.error("Error fetching data:", error);
      setRecommendations(["Произошла ошибка при получении рекомендаций"]);
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    document.body.style.backgroundColor = darkMode ? "#121212" : "#fff";
    document.body.style.color = darkMode ? "#fff" : "#121212";
  }, [darkMode]);

  React.useEffect(() => {
    if (inputText && inputText.length > 0) {
      fetchProductInfo(inputText);
    }
  }, [inputText]);

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
            <Stack spacing={1} sx={{ alignItems: "stretch" }}>
              <TextField
                id="filled-basic-1"
                label="Введите артикул"
                variant="filled"
                value={inputText}
                onChange={(e) => {
                  const value = e.target.value;
                  if (
                    value === "" ||
                    (/^\d+$/.test(value) && value.length <= 20)
                  ) {
                    setInputText(value);
                  }
                }}
                type="text"
                inputProps={{
                  maxLength: 20,
                  pattern: "[0-9]*",
                }}
                sx={{
                  width: "600px",
                }}
              />
              <TextField
                id="filled-basic-2"
                label="Введите поисковый запрос"
                variant="filled"
                value={inputText2}
                onChange={(e) => setInputText2(e.target.value)}
                type="text"
                inputProps={{
                  maxLength: 20,
                }}
                sx={{
                  width: "600px",
                }}
              />
            </Stack>
            <Button
              variant="contained"
              color="primary"
              disableRipple
              disableElevation
              disabled={isLoading}
              sx={{
                minWidth: "200px",
                height: "118px",
              }}
              onClick={() => {
                if (inputText && inputText2) {
                  fetchProductData(inputText);
                } else {
                  if (!inputText) {
                    console.error("Пожалуйста, введите артикул");
                  }
                  if (!inputText2) {
                    console.error("Пожалуйста, введите поисковый запрос");
                  }
                }
              }}
            >
              {isLoading ? "Загрузка..." : "Получить рекомендации"}
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
              {productData ? (
                <Stack
                  direction="row"
                  spacing={3}
                  sx={{
                    alignItems: "flex-start",
                    justifyContent: "space-between",
                  }}
                >
                  <img
                    src={productData.image}
                    alt="Product"
                    style={{
                      maxWidth: "200px",
                      height: "auto",
                      objectFit: "contain",
                    }}
                  />
                  <Stack spacing={1} sx={{ flex: 1 }}>
                    <Typography>ID: {productData.id}</Typography>
                    <Typography>Название: {productData.name}</Typography>
                    <Typography>Рейтинг: {productData.rating}</Typography>
                    <Typography>
                      Дата создания: {productData.create_date}
                    </Typography>
                  </Stack>
                </Stack>
              ) : (
                <Typography>
                  Загрузка данных для артикула {inputText}...
                </Typography>
              )}
            </Paper>
          )}

          {recommendations && (
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
                mt: 2,
              }}
            >
              <Typography variant="h6" sx={{ mb: 2 }}>
                Рекомендации по улучшению позиций:
              </Typography>
              {recommendations.map((rec, index) => (
                <Typography
                  key={index}
                  sx={{
                    whiteSpace: "pre-line",
                    mb: 1,
                  }}
                >
                  {rec}
                </Typography>
              ))}
            </Paper>
          )}
        </Stack>
      </div>
    </ThemeProvider>
  );
}

export default App;
