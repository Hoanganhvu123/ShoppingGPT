import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import './Styles/reset.css';
import ShopContextProvider from './Context/ShopContext.jsx';
import Chatbot from './Components/Chatbot/Chatbot'; // Thêm dòng này

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ShopContextProvider>
      <App />
      <Chatbot /> {/* Thêm dòng này */}  
    </ShopContextProvider>
  </React.StrictMode>
);
