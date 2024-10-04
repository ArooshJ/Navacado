import React from 'react';
import { Link } from 'react-router-dom';

const SignupPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg flex">
        {/* <div className="mr-8">
          <img src="image_url" alt="Signup Illustration" className="w-72" />
        </div> */}
        <div className="text-white">
          <h2 className="text-4xl font-bold mb-4">Create Your Account</h2>
          <p className="text-gray-400 mb-8">Fill in the details below to get started</p>
          <div className="mb-4">
            <input
              type="text"
              placeholder="Enter Username"
              className="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
            />
            <input
              type="email"
              placeholder="Enter Email"
              className="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
            />
            <input
              type="password"
              placeholder="Enter Password"
              className="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button className="w-full bg-green-600 p-3 rounded-lg hover:bg-green-700 transition duration-300">
            Create Account
          </button>
          <div className="mt-4 text-center">
            <p>
              Already have an account?{' '}
              <Link to="/login" className="text-blue-400 hover:text-blue-500 transition duration-300">
                Sign In
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
