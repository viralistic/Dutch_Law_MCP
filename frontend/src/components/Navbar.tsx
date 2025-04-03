
import { Button } from "./ui/button";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="flex justify-between items-center py-4 px-6 md:px-10 bg-[#E7F0F5]/80 backdrop-blur-sm sticky top-0 z-50 border-b border-[#C2D4DB]">
      <div className="flex items-center">
        <Link to="/" className="text-xl font-semibold text-[#161A33]">
          wetMCP.nl
        </Link>
      </div>
      <div className="flex items-center gap-2 md:gap-4">
        <Link 
          to="/about" 
          className="text-[#161A33]/80 hover:text-[#161A33] transition-colors px-3 py-2 rounded-md"
        >
          About
        </Link>
        <Link 
          to="/documentation" 
          className="text-[#161A33]/80 hover:text-[#161A33] transition-colors px-3 py-2 rounded-md"
        >
          Documentation
        </Link>
        <Link 
          to="/repository" 
          className="text-[#161A33]/80 hover:text-[#161A33] transition-colors px-3 py-2 rounded-md"
        >
          Repository
        </Link>
        <Button className="bg-[#161A33] hover:bg-[#2D3252] text-white rounded-md">
          Get Started
        </Button>
      </div>
    </nav>
  );
};

export default Navbar;
