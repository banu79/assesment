import React from "react";

const Message = ({ message }) => {
  return (
    <div
      className={`message ${
        message.sender === "user" ? "user-message" : "bot-message"
      }`}
    >
      <p>{message.text}</p>
    </div>
  );
};

export default Message; // ✅ Ensure default export
