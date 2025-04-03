
import { Button } from "./ui/button";
import { ArrowRight, Github } from "lucide-react";

const GetStartedSection = () => {
  return (
    <section className="py-20 bg-gradient-to-b from-[#E7F0F5] to-[#C2D4DB]/60">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-3xl font-bold text-[#161A33] mb-4">Ready to Get Started?</h2>
        <p className="text-[#161A33]/80 mb-10 max-w-2xl mx-auto">
          Start exploring the Dutch Law MCP framework today. Clone the repository, explore the examples, and contribute to making legal knowledge accessible to everyone.
        </p>
        
        <div className="flex flex-wrap justify-center gap-4">
          <Button className="bg-[#161A33] hover:bg-[#2D3252] text-white px-6 py-6 text-lg rounded-md flex items-center gap-2 shadow-lg hover:shadow-xl transition-all">
            Documentation
            <ArrowRight size={18} />
          </Button>
          <a href="https://github.com/user/dutch-law-mcp" target="_blank" rel="noopener noreferrer">
            <Button variant="outline" className="px-6 py-6 text-lg border-[#C2D4DB] text-[#161A33] bg-white/50 backdrop-blur-sm rounded-md flex items-center gap-2 shadow-md hover:shadow-lg transition-all">
              <Github size={18} />
              GitHub Repository
            </Button>
          </a>
        </div>
      </div>
    </section>
  );
};

export default GetStartedSection;
