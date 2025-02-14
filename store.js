import { configureStore } from "@reduxjs/toolkit";
import messageReducer from "./messageSlice"; // ✅ Ensure correct path

const store = configureStore({
  reducer: {
    messages: messageReducer,
  },
});

export default store; // ✅ Ensure default export
