import logo from './logo.svg';
import './App.css';

import { BrowserRouter, Routes, Route} from "react-router-dom";
import Car from './pages/Car'
import Cars from './pages/Cars'
import NewCar from './pages/NewCar'
import Home from './pages/Home'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="cars" element={<Cars />} />
        <Route path="new" element={<NewCar />} />
        <Route path="cars/:id" element={<Car />} />
        <Route path="*" element={
          <main style={{ padding: "1rem" }}>
            <p>There's nothing here!</p>
          </main>
        }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
