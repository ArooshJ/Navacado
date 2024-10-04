import React from 'react';

export default function StudentPageButtons({setTable}) {
  const Attendance = ()=>{
     setTable("Attendance");
  }
  const TimeTable = ()=>{
    setTable("Timetable");
 }
 const Holiday= ()=>{
  setTable('Holidays');
}



  return (

    <div className="flex space-x-4 my-4 w-full justify-center">
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow-md">
        No of Courses
      </button>
      <button className="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded shadow-md" onClick={TimeTable}>
        See TimeTable
      </button>
      <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded shadow-md" onClick={Holiday}>
        Next Holiday
      </button>
      <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded shadow-md" onClick={Attendance}>
        Attendance
      </button>
    </div>
  );
}
