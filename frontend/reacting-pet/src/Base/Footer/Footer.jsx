import styles from "./Footer.module.css";

function Footer() {
  return (
    <footer className={styles.footer}>
      <p>
        For additional information please contact us:
        <a href="mailto:petawebmail@gmail.com"> Petawebmail@gmail.com</a>
      </p>
    </footer>
  );
}

export default Footer;
