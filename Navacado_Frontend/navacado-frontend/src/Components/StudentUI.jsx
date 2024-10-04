import React from 'react'

export default function StudentUI() {
  return (
    <div className='w-full h-screen border-2 border-red-500 bg-gray-800 text-white flex flex-col justify-center items-center py-2 ' >
      <div className="w-4/5 border-2 flex justify-evenly items-center rounded">
         <div className="border-2 border-green-200 flex justify-evenly items-center m-2 p-2 rounded">Profile </div>
         <div className="w-2/3 border-2 border-green-200 flex justify-center items-center m-2 p-2 flex-col justify-self-end rounded "> 
          Info
          <div className="border-2 border-green-200 flex justify-center items-center m-1 p-1 rounded-lg">Name : Lorem, ipsum dolor.</div>
          <div className="border-2 border-green-200 flex justify-center items-center m-1 p-1 rounded-lg"> 
            UID : Lorem ipsum dolor sit.
          </div>
          <div className="border-2 border-green-200 flex justify-center items-center m-1 p-1 rounded-lg">Class Division Batch</div>
            
          <button className="bg-gray-800 hover:bg-gray-500 border-2 border-blue-200 rounded-2xl mt-2"> View TimeTable</button>
          <button className="bg-gray-800 hover:bg-gray-500 border-2 border-blue-200 rounded-2xl mt-1 "> Edit profile</button>
                                               
          
         </div>
      </div>
      <div className="w-4/5 border-2 border-red-300 py-2 my-2">
        Your attendance
        
      </div>

      
       
    </div>
  )
}
