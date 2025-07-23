import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Header from './components/common/Header';
import LoginForm from './components/auth/LoginForm';
import BorrowerDashboard from './components/borrower/BorrowerDashboard';
import LenderDashboard from './components/lender/LenderDashboard';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const AppContent: React.FC = () => {
  const { user } = useAuth();

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route path="/login" element={
            user ? (
              <Navigate to={user.role === 'borrower' ? '/borrower' : '/lender'} replace />
            ) : (
              <LoginForm />
            )
          } />
          
          <Route path="/borrower" element={
            <ProtectedRoute>
              <Header />
              <BorrowerDashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/lender" element={
            <ProtectedRoute>
              <Header />
              <LenderDashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/" element={
            <Navigate to={user ? (user.role === 'borrower' ? '/borrower' : '/lender') : '/login'} replace />
          } />
        </Routes>
      </div>
    </Router>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;