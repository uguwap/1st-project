import React from "react";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<h1>Главная страница</h1>} />
      <Route path="*" element={<h2>Страница не найдена</h2>} />
    </Routes>
  );
}

export default App;

