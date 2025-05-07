import React from "react";
import { createRoot } from "react-dom/client";
import ChatWidget from "./components/ChatWidget/ChatWidget";

const container = document.getElementById("chat-widget");
if (container) {
  const root = createRoot(container);
  root.render(<ChatWidget />);
}
