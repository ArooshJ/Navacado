import React from 'react';

export default function AttendanceStatus() {
  const attendanceData = [
    { course: 'Mathematics', attended: 24, totalLectures: 30 },
    { course: 'Physics', attended: 18, totalLectures: 28 },
    { course: 'Chemistry', attended: 20, totalLectures: 25 },
    // Add more courses as needed
  ];

  return (
    <div className="w-full bg-white p-6 rounded-md shadow-md">
      <h2 className="text-lg font-bold mb-4">Coursewise Attendance Status</h2>
      <table className="min-w-full bg-gray-100">
        <thead>
          <tr className="bg-gray-300">
            <th className="py-2 px-4">Course</th>
            <th className="py-2 px-4">Lectures Attended</th>
            <th className="py-2 px-4">Total Lectures</th>
            <th className="py-2 px-4">Percentage</th>
          </tr>
        </thead>
        <tbody>
          {attendanceData.map((course, index) => (
            <tr key={index} className="bg-white border-b">
              <td className="py-2 px-4">{course.course}</td>
              <td className="py-2 px-4">{course.attended}</td>
              <td className="py-2 px-4">{course.totalLectures}</td>
              <td className="py-2 px-4">{((course.attended / course.totalLectures) * 100).toFixed(2)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
