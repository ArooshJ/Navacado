import React from 'react'
import { Link, Navigate } from 'react-router-dom'
export default function Navbar({setLogin}) {
  
  const handleLogout = ()=>{
    
    setLogin(false)
  }
  return (
    <nav className="bg-gray-900 p-4  w-full">
    <div className="container mx-auto flex justify-between items-center">
      <Link to="/" className="text-white text-xl font-bold hover:text-gray-100">Navacado</Link>
      <div className="space-x-4">
        <Link to="/" className="text-white hover:text-gray-300">Home</Link>
        <Link to="/about" className="text-white hover:text-gray-300">About</Link>
        <Link to="/students" className="text-white hover:text-gray-300">Your Profile</Link>
        <button className="text-white hover:text-gray-300" onClick={handleLogout}>Logout</button>
      </div>
    </div>
  </nav>
  )
}
