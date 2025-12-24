import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import Header from './components/Header';
import UploadPage from './pages/UploadPage';
import ProcessingPage from './pages/ProcessingPage';
import DashboardPage from './pages/DashboardPage';
import PodcastDetailsPage from './pages/PodcastDetailsPage';
import logger from "./utils/logger";

const App = () => {

  // ✅ FRONTEND LOAD LOG (ADDED)
  useEffect(() => {
    logger.info("Frontend application loaded");
  }, []);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background">
        <Header />
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/processing" element={<ProcessingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/podcast/:id" element={<PodcastDetailsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
