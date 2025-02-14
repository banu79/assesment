import axios from "axios";

const BASE_URL = "http://localhost:8000"; // Ensure this matches your FastAPI URL

export const sendMessageToBackend = async (message) => {
  try {
    const response = await axios.get(`${BASE_URL}/query`, {
      params: { query: message }, // Ensure query is passed as a simple string
    });
    return response.data;
  } catch (error) {
    console.error("API error:", error);
    return { response: "Sorry, something went wrong." };
  }
};
