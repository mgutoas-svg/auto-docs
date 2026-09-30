import { useState, useEffect } from 'react'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }, [token])

  return (
    <div className="min-h-screen bg-gray-50">
      {!token ? (
        <Login onLogin={setToken} />
      ) : (
        <Dashboard token={token} onLogout={() => setToken(null)} />
      )}
    </div>
  )
}

export default App
