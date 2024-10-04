import React ,{Fragment, useContext}from 'react'
import {Route, Navigate} from 'react-router-dom'
import AuthContext from './Contexts/AuthContext';
export default function PrivateRoute({children, ...rest}) {
    // console.log('privateroute')
    const isAuthenticated = true;
    let {user} = useContext(AuthContext) 
  return (
   user?<>{children}</>:<Navigate to ='/login/'/> 
  )
}
