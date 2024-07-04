import styles from './Base.module.css'
import Navbar from '../Navbar/Navbar.jsx'
import Home from '../Home/Home.jsx'
import Footer from '../Footer/Footer.jsx'

function Base() {

  return (
    <div className={styles.base}>
      <Navbar />
      <div className={styles.homeBg}>
      <Home />
      </div>
      <Footer />
    </div>
  )
}

export default Base
