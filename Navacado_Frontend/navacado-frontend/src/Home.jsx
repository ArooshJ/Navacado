import React from 'react';

function Home() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header Section */}
      <header className="bg-gray-900 text-white py-16">
        <div className="container mx-auto px-6">
            <h1 className="text-4xl font-bold mb-4">Navacado</h1>
          <h1 className="text-4xl font-bold mb-4">
            Attendance Management Made Simple
          </h1>
          <p className="text-lg mb-8">
            Track, manage, and report attendance effortlessly with real-time syncing.
          </p>
          <div>
            <button className="bg-white text-indigo-600 font-semibold py-2 px-4 rounded-lg mr-4 hover:bg-gray-200">
              Get Started
            </button>
            <button className="bg-indigo-500 font-semibold py-2 px-4 rounded-lg hover:bg-indigo-700">
              Login
            </button>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section className="py-16 bg-gray-200">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-8">
            Key Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 border rounded-lg shadow-sm bg-gray-50">
              <h3 className="font-bold text-xl mb-2">Automated Attendance</h3>
              <p>Track attendance automatically for students and employees with just a few clicks.</p>
            </div>
            <div className="p-6 border rounded-lg shadow-sm bg-gray-50">
              <h3 className="font-bold text-xl mb-2">Real-Time Reporting</h3>
              <p>Generate and export detailed attendance reports instantly.</p>
            </div>
            <div className="p-6 border rounded-lg shadow-sm bg-gray-50">
              <h3 className="font-bold text-xl mb-2">User Management</h3>
              <p>Easy-to-use admin interface to manage students, teachers, and staff.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-gray-100">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-8">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="p-6 border rounded-lg shadow-sm bg-white">
                <h3 className="font-bold text-xl mb-2">Step 1: Login</h3>
                <p>Access your dashboard by logging into the system.</p>
              </div>
            </div>
            <div>
              <div className="p-6 border rounded-lg shadow-sm bg-white">
                <h3 className="font-bold text-xl mb-2">Step 2: Mark Attendance</h3>
                <p>Take attendance easily using the system’s automated tools.</p>
              </div>
            </div>
            <div>
              <div className="p-6 border rounded-lg shadow-sm bg-white">
                <h3 className="font-bold text-xl mb-2">Step 3: View Reports</h3>
                <p>Generate attendance reports for any class, anytime.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-indigo-600 text-white py-6">
        <div className="container mx-auto text-center">
          <p>&copy; 2024 Attendance Management System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default Home;

