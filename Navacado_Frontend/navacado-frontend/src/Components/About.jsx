import React from 'react';

function About() {
  return (
    <div className="min-h-screen bg-gray-900">
      {/* Introduction Section */}
      <section className="bg-gray-900 py-16">
        <div className="container mx-auto px-6">
          <h1 className="text-4xl font-bold text-center text-indigo-300 mb-4">
            About Navacado
          </h1>
          <p className="text-lg text-center text-gray-700 mb-8">
            Our system is designed to streamline the process of tracking attendance for schools, universities, and businesses.
            Built with simplicity and efficiency in mind, it's the ultimate tool for managing attendance and generating real-time reports.
          </p>
        </div>
      </section>

      {/* Mission and Vision Section */}
      <section className="py-16 bg-gray-100">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
            Our Mission and Vision
          </h2>
          <p className="text-lg text-center text-gray-700 max-w-4xl mx-auto">
            Our mission is to provide an easy-to-use, scalable solution that empowers institutions and businesses to manage their
            attendance seamlessly. Our vision is to revolutionize attendance management by making it fully automated, reducing manual effort
            and human error.
          </p>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
            Why Choose Navacado?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 border rounded-lg shadow-sm bg-gray-50">
              <h3 className="font-bold text-xl mb-2">Ease of Use</h3>
              <p>Our intuitive interface makes it easy for anyone to track attendance and generate reports with just a few clicks.</p>
            </div>
            <div className="p-6 border rounded-lg shadow-sm bg-gray-50">
              <h3 className="font-bold text-xl mb-2">Real-Time Syncing</h3>
              <p>Data is synced in real-time, allowing for up-to-date attendance tracking and reporting without delays.</p>
            </div>
            <div className="p-6 border rounded-lg shadow-sm bg-gray-50">
              <h3 className="font-bold text-xl mb-2">Customizable Features</h3>
              <p>Our system is flexible and can be customized to fit the specific needs of any institution or organization.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section (Optional) */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
            Meet the Team
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 border rounded-lg shadow-sm bg-white text-center">
              <h3 className="font-bold text-xl mb-2">John Doe</h3>
              <p className="text-gray-700">Founder & CEO</p>
            </div>
            <div className="p-6 border rounded-lg shadow-sm bg-white text-center">
              <h3 className="font-bold text-xl mb-2">Jane Smith</h3>
              <p className="text-gray-700">Lead Developer</p>
            </div>
            <div className="p-6 border rounded-lg shadow-sm bg-white text-center">
              <h3 className="font-bold text-xl mb-2">Bob Johnson</h3>
              <p className="text-gray-700">UI/UX Designer</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="bg-indigo-600 text-white py-6">
        <div className="container mx-auto text-center">
          <p>&copy; 2024 Attendance Management System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default About;
