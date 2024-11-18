import './Base.css'
import Navbar from './Navbar/Navbar.jsx'
import Home from './Home/Home.jsx'
import Footer from './Footer/Footer.jsx'

const Base = () => {

  return (
    <div className="base">
      <Navbar />
      <div className="homeBg">
      <Home />
      </div>
      {/* <Footer /> */}
    </div>
  )
}

export default Base
