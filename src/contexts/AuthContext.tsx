import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { mockUsers } from '../data/mockData';
import API_BASE_URL from './../..//config';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, char) => char.toUpperCase());
}

function convertKeysToPascalCase(obj: Record<string, any>): Record<string, any> {
  const newObj: Record<string, any> = {};

  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const pascalKey = snakeToCamel(key);
      newObj[pascalKey] = obj[key];
    }
  }

  return newObj;
}

function convertListToPascalCase(data: Record<string, any>[]): Record<string, any>[] {
  return data.map(item => convertKeysToPascalCase(item));
}





export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored session
    const storedUser = null;
    // localStorage.getItem('kishti-user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true);
  
    try {
      const response = await fetch(`${API_BASE_URL}/sign-in?email=${email}&password=${password}`, {
        method: 'POST', // or 'POST' if your backend expects it
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      if (response.ok) {
        const user = await response.json();

        console.log("user",user);
        try{
          const res = await fetch(`${API_BASE_URL}/getUserDetails/${user.user_id}`);

          if(res.ok){
            const user1 = await res.json();
            const temp = {
              ...user1.user,
              profile: convertKeysToPascalCase(user1.borrower_profile),
              loans: convertListToPascalCase(user1.loans),
              emiWallet: convertKeysToPascalCase(user1.emi_wallet),
              transactions: convertListToPascalCase(user1.transactions),
              emiPayments: convertListToPascalCase(user1.emi_payments),
              

            }; 
            console.log('temp', temp)
            setUser(temp);
          }else{console.error("hey error")}

        } catch(e){
          console.error('Login failed with status:');
        }

        
        // localStorage.setItem('kishti-user', JSON.stringify(user));
        return true;
      } else {
        console.error('Login failed with status:', response.status);
      }
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setIsLoading(false);
    }
  
    return false;
  };

  // const login = async (email: string, password: string): Promise<boolean> => {
  //   setIsLoading(true);
    
  //   // Simulate API call
  //   await new Promise(resolve => setTimeout(resolve, 1000));
    
  //   const foundUser = mockUsers.find(u => u.email === email);
  //   if (foundUser && password === 'password') {
  //     setUser(foundUser);
  //     localStorage.setItem('kishti-user', JSON.stringify(foundUser));
  //     setIsLoading(false);
  //     return true;
  //   }
    
  //   setIsLoading(false);
  //   return false;
  // };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('kishti-user');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};