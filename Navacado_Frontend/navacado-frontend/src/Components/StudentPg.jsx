import React, { useState } from 'react'
import ProfileCard from './ProfileCard'
import StudentPageButtons from './StudentPageButtons'
import AttendanceStatus from './AttendanceStatus'
import Timetable from './Timetable'

export default function StudentPg() {
  
  const [table, setTable] = useState('Attendance')

  return (
    <div>
       <ProfileCard />

       <StudentPageButtons setTable={setTable}/>
       
       {
          table == 'Attendance' ? (
            <>
            <AttendanceStatus />
            </>
          ) : 
          table == 'Timetable' ? (
            <>
              <Timetable />
            </>
          ) :
         ( <>
             <Timetable/>
          </>)
       }

  

    
    </div>
  )
}
