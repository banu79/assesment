import React, { useState, useEffect } from "react";
import {
  Box,
  TextField,
  IconButton,
  CircularProgress,
  Button,
  Typography,
  Paper,
} from "@mui/material";
import { Send as SendIcon, History as HistoryIcon } from "@mui/icons-material";
import axios from "axios";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    const welcomeMessage = {
      text: "Welcome! I can assist you with services, products, and suppliers. How can I help today?",
      sender: "bot",
    };
    setMessages([welcomeMessage]);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: "user" };
    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.get(
        `http://localhost:8000/query?query=${input}`
      );
      let botResponse;

      if (response.data.products) {
        botResponse = response.data.products
          .map(
            (product) =>
              `Product: ${product.name}\nPrice: ${product.price}\nSupplier: ${product.supplier}`
          )
          .join("\n\n");
      } else {
        botResponse = response.data.response;
      }

      const botMessage = {
        text: `Here's what I found:\n${botResponse}\n\nThank you for reaching out!`,
        sender: "bot",
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { text: "Error fetching response. Please try again!", sender: "bot" },
      ]);
    }
    setLoading(false);
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        maxWidth: 500,
        mx: "auto",
        bgcolor: "background.default",
        p: 2,
      }}
    >
      <Paper
        sx={{ flex: 1, overflowY: "auto", p: 2, mb: 2, bgcolor: "grey.100" }}
      >
        {messages.map((msg, index) => (
          <Box
            key={index}
            sx={{
              p: 1.5,
              mb: 1,
              maxWidth: "75%",
              borderRadius: 2,
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              bgcolor: msg.sender === "user" ? "primary.main" : "grey.300",
              color: msg.sender === "user" ? "white" : "black",
            }}
          >
            {msg.text.split("\n").map((line, i) => (
              <Typography key={i} variant="body1">
                {line}
              </Typography>
            ))}
          </Box>
        ))}
      </Paper>

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1,
          bgcolor: "background.paper",
          p: 1,
          borderRadius: 2,
        }}
      >
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Ask me about products or suppliers..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <IconButton color="primary" onClick={sendMessage} disabled={loading}>
          {loading ? <CircularProgress size={24} /> : <SendIcon />}
        </IconButton>
      </Box>

      <Button
        variant="contained"
        color="secondary"
        startIcon={<HistoryIcon />}
        sx={{ mt: 2 }}
        onClick={() => setShowHistory(!showHistory)}
      >
        {showHistory ? "Hide History" : "Show History"}
      </Button>

      {showHistory && (
        <Paper sx={{ mt: 2, p: 2, bgcolor: "grey.200" }}>
          <Typography variant="h6">Conversation History</Typography>
          {messages.map((msg, index) => (
            <Typography
              key={index}
              sx={{ color: msg.sender === "user" ? "blue" : "black" }}
            >
              {msg.sender === "user" ? "You: " : "Bot: "} {msg.text}
            </Typography>
          ))}
        </Paper>
      )}
    </Box>
  );
};

export default Chatbot;
