import {useState, useEffect} from "react"
import Layout from "../components/Layout"
import Card from "../components/Card"
import Loading from "../components/Loading";

let BASE_URL = "https://secret-river-09896.herokuapp.com/cars"
//let BASE_URL = "http://localhost:8000/cars"

const Cars = () => {

  const [cars, setCars] = useState([])
  const [brand, setBrand] = useState('')
  const [isPending, setIsPending] = useState(true)
  const [page, setPage] = useState(1)

  const handleChangeBrand = (ev) => {
    setCars([])
    setBrand(ev.target.value)
    setIsPending(true)
  }

  const handleChangePage = (ev) => {
    setCars([])
    setPage(ev.target.value)
    setIsPending(true)
  }

  useEffect(() => {
    fetch(`${BASE_URL}?brand=${brand}&page=${page}`)
      .then(response => response.json())
      .then(json => {
        setCars(json)
        setIsPending(false)
      })
  }, [brand, page])

  return (
    <Layout>
      <h2 className="font-bold font-mono text-lg text-center my-4">
        Cars - {brand ? brand : "all brands"}
      </h2>
      <div className="mx-8">
        <label htmlFor="cars">Choose a brand: </label>
        <select name="cars" id="cars" onChange={handleChangeBrand}>
          <option value="">All cars</option>
          <option value="Fiat">Fiat</option>
          <option value="Citroen">Citroen</option>
          <option value="Renault">Renault</option>
          <option value="Opel">Opel</option>
        </select>
        <label htmlFor="page">Choose a page: </label>
        <select name="page" id="page" onChange={handleChangePage}>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
      </div>
      <div className="mx-8">
        {isPending && <Loading brand={brand}/>}
        <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
          {cars && cars.map((el) => <Card key={el._id} car={el}/>)}
        </div>
      </div>
    </Layout>
  )
}

export default Cars
