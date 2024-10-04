import React from 'react';

export default function ProfileCard() {
  return (
    <div className="w-full  bg-gray-200 p-4 rounded-md shadow-md flex justify-between items-center">
      <div className="flex flex-col justify-self - center">
        <h2 className="text-xl font-bold text-gray-800">John Doe</h2>
        <p className="text-gray-600">Student ID: 2022700019</p>
        <p className="text-gray-600">TE CSE DS, Batch B</p>
      </div>

      <div className="w-16 h-16 rounded-full bg-blue-500 flex justify-center items-center text-white justify-self-end">
        {/* Profile Image Placeholder */}
        <span className="text-2xl">JD</span>
      </div>

    </div>
  );
}

