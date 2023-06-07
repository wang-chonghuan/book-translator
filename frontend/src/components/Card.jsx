import { Link } from "react-router-dom"

const Card = ({ car }) => {
  let { brand, price, make, year, km, cm3, _id } = car
  return (
    <Link to={`/cars/${_id}`}>
      <div className="flex flex-col shadow-lg p-5 bg-FarmWhite rounded-lg transition ease-in-out hover:scale-105 duration-300 font-mono">
        <div className="font-bold text-center text-lg text-FarmNavy">
          <span className="text-FramLim">{brand}</span> {make}
        </div>
        <div>Year: {year}</div>
        <div>
          Price: <span className="font-semibold text-orange-600">{price}</span>
        </div>
        <div>Km: {km}</div>
        <div>Engine: {cm3}cm3</div>
      </div>
    </Link>
  )
}

export default Card

