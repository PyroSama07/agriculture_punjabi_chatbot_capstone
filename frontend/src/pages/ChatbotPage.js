import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styling/ChatbotPage.css";

function ChatbotPage({ onLogout }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const token = localStorage.getItem("token"); // Retrieve token from localStorage

  useEffect(() => {
    fetchMessages();
  }, []);

  // Function to fetch messages
  const fetchMessages = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_KEY}/get_all_message`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMessages(response.data);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  // Function to send a new message
  const sendMessage = async () => {
    if (!newMessage.trim()) return;
    try {
      await axios.post(
        `${process.env.REACT_APP_API_KEY}/send_message`,
        { msg: newMessage },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setNewMessage(""); // Clear the input field
      fetchMessages(); // Refresh the messages
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  // Function to delete all messages
  const deleteAllMessages = async () => {
    try {
      await axios.delete(
        `${process.env.REACT_APP_API_KEY}/delete_all_messages`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMessages([]); // Clear messages from state
      alert("All messages have been deleted successfully!");
    } catch (error) {
      console.error("Error deleting messages:", error);
      alert("Failed to delete messages. Please try again.");
    }
  };

  // Function to handle logout
  const handleLogout = async () => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_KEY}/logout`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      localStorage.removeItem("token"); // Remove token from localStorage
      onLogout(); // Callback to handle logout logic
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <div className="chatbot-container">
      <h1>Chatbot</h1>
      <div className="chat-box">
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <div
              key={msg.id}
              className={`chat-message ${
                msg.sender ? "bot-message" : "user-message"
              }`}
            >
              <span className="message-content">{msg.msg}</span>
              <span className="message-time">
                {new Date(msg.time_stamp).toLocaleTimeString()}
              </span>
            </div>
          ))
        ) : (
          <p>No messages yet. Start the conversation!</p>
        )}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />

        <button type="submit" onClick={sendMessage}>
          Send
        </button>

        <button className="delete-button" onClick={deleteAllMessages}>
          Delete All Messages
        </button>
      </div>
      <button className="logout-button" onClick={handleLogout}>
        Logout
      </button>
      \
    </div>
  );
}

export default ChatbotPage;
