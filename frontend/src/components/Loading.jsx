import React from 'react'

const Loading = ({brand}) => {
  return (
    <div className="flex flex-col justify-center items-center absolute
                    opacity-90 bg-red-500 text-white text-lg
                    top-0 left-0 right-0 bottom-0">
      <h2 className="text-5xl">
        Loading cars, brand:{brand ? brand : 'any'}...
      </h2>
    </div>)
}

export default Loading
