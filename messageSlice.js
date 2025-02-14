import { createSlice } from "@reduxjs/toolkit";

const messageSlice = createSlice({
  name: "messages",
  initialState: [],
  reducers: {
    sendMessage: (state, action) => {
      state.push({ sender: "user", text: action.payload });
    },
    receiveMessage: (state, action) => {
      state.push({ sender: "bot", text: action.payload });
    },
  },
});

export const { sendMessage, receiveMessage } = messageSlice.actions;
export default messageSlice.reducer;
