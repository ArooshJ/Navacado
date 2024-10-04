import React from 'react';
import { Link } from 'react-router-dom';

const LoginPage = ({setLogin}) => {
    const handleLogin = ()=>{
        setLogin(true)
    }

    return (
        <div className="min-h-screen min-w-screen mx-0 px-0 flex items-center justify-center bg-gray-900">
            <div className="bg-gray-800 p-8 rounded-lg shadow-lg flex">
                <div className="mr-8">
                    <img src="image_url" alt="Login Illustration" className="w-72" />
                </div>
                
                <div className="text-white">
                    <h2 className="text-4xl font-bold mb-4">Sign In to Your Account</h2>
                    <p className="text-gray-400 mb-8">Select Your Role</p>
                    <div className="flex items-center space-x-4 mb-6">
                        <label className="flex items-center space-x-2">
                            <input type="radio" name="role" className="form-radio text-red-500" />
                            <span>Admin</span>
                        </label>
                        <label className="flex items-center space-x-2">
                            <input type="radio" name="role" className="form-radio text-green-500" />
                            <span>Teacher</span>
                        </label>
                        <label className="flex items-center space-x-2">
                            <input type="radio" name="role" className="form-radio text-blue-500" />
                            <span>Student</span>
                        </label>
                    </div>
                    
                    <div className="mb-4">
                        <input
                            type="text"
                            placeholder="Enter Username"
                            className="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
                        />
                        <input
                            type="password"
                            placeholder="Enter Password"
                            className="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>
                    <button className="w-full bg-red-600 p-3 rounded-lg hover:bg-red-700 transition duration-300" onClick={handleLogin}>
                        Sign In
                    </button>
                    <div className="mt-4 text-center">
                        <p>
                            Don't have an account?{' '}
                            <Link to="/signup" className="text-blue-400 hover:text-blue-500 transition duration-300">
                                Create one
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
