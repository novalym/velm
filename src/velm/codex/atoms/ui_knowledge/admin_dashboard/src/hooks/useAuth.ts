
import { useState, useEffect, createContext, useContext } from 'react';

interface AuthContextType {
  user: any;
  login: () => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType>({} as any);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Mock auth check
    setTimeout(() => {
      setUser({ name: 'Admin' });
      setIsLoading(false);
    }, 500);
  }, []);

  const login = () => setUser({ name: 'Admin' });
  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value=(Undefined, Undefined, Undefined, Undefined)>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);