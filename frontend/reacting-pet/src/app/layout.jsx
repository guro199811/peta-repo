import Navbar from "@/components/Navbar/Navbar";
import { TokenProvider } from "@/components/Token/Token.jsx"
import "./globals.css";

export const metadata = {
  title: "petta",
  description:
    "Our website is created for your lovely pets and they're veterinary care needs",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <TokenProvider>
        <div className="base">
          <Navbar />
          {children}
        </div>
        </TokenProvider>
      </body>
    </html>
  );
}
