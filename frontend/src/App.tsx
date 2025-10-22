import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FeedDashboard from "./Pages/FeedDashboard";
import AddSource from "./pages/AddSource";
import ManageSources from "./pages/ManageSources";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FeedDashboard />} />
        <Route path="/add-source" element={<AddSource />} />
        <Route path="/manage-sources" element={<ManageSources />} />
      </Routes>
    </Router>
  );
}

export default App;