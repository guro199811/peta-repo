import React from "react";
import ReactDOM from "react-dom/client";
import Base from "./Base/Base.jsx";
import { TokenProvider } from "./Token/Token.jsx";
import "./main.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <TokenProvider>
      <Base />
    </TokenProvider>
  </React.StrictMode>
);
