export default function Timetable() {
    const timetableData = [
      { day: 'Monday',from: '9:00 AM ',to: '10:00 AM', lecture: 'Mathematics' },
      { day: 'Monday', from: '10:00 AM ',to:' 11:00 AM', lecture: 'Physics' },
      { day: 'Tuesday', from: '9:00 AM', to:'10:00 AM', lecture: 'Chemistry' },
      // Add more days and time slots as needed
    ];
  
    return (
      <div className="bg-gray-100 p-6 rounded-md shadow-md w-full">
        <h2 className="text-lg font-bold mb-4">Timetable</h2>
        <div className="space-y-2">
          <div className="grid grid-cols-4 gap-2 white p-4 rounded-md shadow-md font-bold">
              <span className="text-gray-700">Day</span>
              <span className="text-gray-700">From</span>
              <span className="text-gray-700">To</span>
              <span className="text-gray-700">Lecture</span>
            </div>
          {timetableData.map((item, index) => (
            <div key={index} className="grid grid-cols-4 gap-2  white p-4 rounded-md shadow-md">
              <span className="text-gray-700">{item.day}</span>
              <span className="text-gray-700">{item.from}</span>
              <span className="text-gray-700">{item.to}</span>
              <span className="text-blue-500">{item.lecture}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }