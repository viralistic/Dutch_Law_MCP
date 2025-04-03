
import { Button } from "./ui/button";
import { ArrowRight, Github } from "lucide-react";
import { Link } from "react-router-dom";
import SearchBar from "./SearchBar";

const Hero = () => {
  return (
    <div className="relative overflow-hidden bg-gradient-to-b from-[#C2D4DB] to-[#E7F0F5]">
      {/* Background shapes */}
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-[#E7F0F5] rounded-full opacity-50 blur-3xl"></div>
      <div className="absolute top-1/2 -left-24 w-64 h-64 bg-[#C2D4DB] rounded-full opacity-50 blur-3xl"></div>
      
      <div className="container mx-auto px-6 py-16 md:py-24 relative z-10">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-[#161A33] mb-6 text-gradient">
            Dutch Law Modern Context Protocol
          </h1>
          <p className="text-xl text-[#161A33]/80 mb-10 leading-relaxed">
            An accessible framework for understanding Dutch legislation, making legal knowledge available to everyone, not just legal professionals.
          </p>
          
          {/* SearchBar component moved below the title */}
          <SearchBar />
          
          <div className="flex flex-wrap justify-center gap-4 mt-10">
            <Link to="/documentation">
              <Button className="bg-[#161A33] hover:bg-[#2D3252] text-white px-6 py-6 text-lg rounded-md flex items-center gap-2 shadow-lg hover:shadow-xl transition-all">
                Get Started
                <ArrowRight size={18} />
              </Button>
            </Link>
            <a href="https://github.com/user/dutch-law-mcp" target="_blank" rel="noopener noreferrer">
              <Button variant="outline" className="px-6 py-6 text-lg border-[#C2D4DB] text-[#161A33] bg-white/50 backdrop-blur-sm rounded-md flex items-center gap-2 shadow-md hover:shadow-lg transition-all">
                <Github size={18} />
                View on GitHub
              </Button>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
