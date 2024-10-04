import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './Components/Navbar'
import LoginPage from './Components/LoginPage'
import SignupPage from './Components/SignupPage'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import StudentUI from './Components/StudentUI'
import Profile from './Components/Profile'
import StudentPg from './Components/StudentPg'
import Home from './Home'
import About from './Components/About'

function App() {
  const [count, setCount] = useState(0)
  const [login, setLogin] = useState(false)

  return (

      <Router>
     
       <Navbar setLogin = {setLogin}/> 
      


        <Routes>
{        login ? (
          /* <Route path="/" element={<div>
          <h1 className='text-3l font-bold underline'>
            Hello Tailwind + React
          </h1>
          </div>} /> */
          /* <Route path="/about" element={<About />} />
          <Route path="/services" element={<Services />} />
          <Route path="/contact" element={<Contact />} /> */
            /* <Route path="/" element={<LoginPage />} /> */
          <>
        <Route path="login/" element={<LoginPage />} />
         <Route path="signup/" element={<SignupPage />} />
        <Route path="students/" element={<StudentPg />} />
        <Route path="profile/" element={<Profile />} />
        <Route path="about/" element={<About/>} />

        <Route path="" element={<Home/>} />


          </>  
         

      )
 
       :

       (
        <>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="" element={<LoginPage setLogin={setLogin} />} />
        </>
    
       )
}
       </Routes>
      </Router>

  )
  
}

export default App
