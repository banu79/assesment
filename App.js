// src/App.js
import React from "react";
import Chatbot from "./components/Chatbot";
import { Provider } from "react-redux";
import store from "./redux/store"; // Your redux store setup

const App = () => {
  return (
    <Provider store={store}>
      <div className="App">
        <Chatbot />
      </div>
    </Provider>
  );
};

export default App;
