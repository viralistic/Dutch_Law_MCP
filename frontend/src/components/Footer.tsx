
import { Button } from "./ui/button";
import { MessageCircle } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-[#E7F0F5] border-t border-[#C2D4DB] py-10 px-6 md:px-10">
      <div className="container mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-[#161A33]">Dutch Law MCP</h3>
            <p className="text-[#161A33]/70 text-sm">
              A structured framework for contextualizing, understanding, and applying Dutch legislation, designed for AI agents and legal professionals.
            </p>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-[#161A33]">Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="https://github.com/user/dutch-law-mcp" className="text-[#161A33]/80 hover:text-[#161A33] hover:underline">
                  GitHub Repository
                </a>
              </li>
              <li>
                <a href="https://viralistic.nl" className="text-[#161A33]/80 hover:text-[#161A33] hover:underline">
                  viralistic.nl
                </a>
              </li>
              <li>
                <a href="https://t.me/vrlstc" className="text-[#161A33]/80 hover:text-[#161A33] hover:underline flex items-center gap-2">
                  <MessageCircle size={16} /> @vrlstc
                </a>
              </li>
            </ul>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-[#161A33]">Support</h3>
            <p className="text-[#161A33]/70 text-sm">
              If you find this project useful, consider supporting the developer.
            </p>
            <a href="https://buymeacoffee.com/marrallisa" target="_blank" rel="noopener noreferrer">
              <Button variant="outline" className="flex items-center gap-2 bg-white/50 border-[#C2D4DB] text-[#161A33] hover:bg-white/70">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
                  <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
                  <line x1="6" y1="1" x2="6" y2="4"></line>
                  <line x1="10" y1="1" x2="10" y2="4"></line>
                  <line x1="14" y1="1" x2="14" y2="4"></line>
                </svg>
                Buy me a coffee
              </Button>
            </a>
          </div>
        </div>
        
        <div className="mt-10 pt-6 border-t border-[#C2D4DB] text-center">
          <p className="text-[#161A33]/70 text-sm">
            © {new Date().getFullYear()} Dutch Law MCP by Marrallisa Kreijkes. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
