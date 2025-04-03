
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { GitBranch, GitFork, GithubIcon, Star } from "lucide-react";

const Repository = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow py-16 bg-slate-50">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-slate-800 mb-10">GitHub Repository</h1>
            
            <Card className="border border-slate-200 rounded-lg p-6 bg-white mb-8">
              <CardContent className="p-0 mb-6">
                <div className="flex items-center mb-4">
                  <GithubIcon className="h-8 w-8 text-slate-800 mr-3" />
                  <h2 className="text-2xl font-semibold text-slate-800">Dutch Law MCP</h2>
                </div>
                
                <p className="text-slate-600 mb-6">
                  An unofficial MCP server for Dutch Law to get reliable output for your AI agents.
                </p>
                
                <div className="flex flex-wrap gap-4 mb-6">
                  <div className="flex items-center text-slate-600 text-sm">
                    <Star className="h-4 w-4 mr-1 text-yellow-500" />
                    <span>Stars: 32</span>
                  </div>
                  <div className="flex items-center text-slate-600 text-sm">
                    <GitFork className="h-4 w-4 mr-1" />
                    <span>Forks: 8</span>
                  </div>
                  <div className="flex items-center text-slate-600 text-sm">
                    <GitBranch className="h-4 w-4 mr-1" />
                    <span>Branches: 3</span>
                  </div>
                </div>
                
                <div className="border border-slate-200 rounded-md p-4 bg-slate-50">
                  <h3 className="font-medium text-slate-800 mb-2">Repository Structure</h3>
                  <ul className="list-disc list-inside space-y-1 text-slate-600">
                    <li><strong>docs/</strong>: Documentation on how to use and contribute to the MCP framework</li>
                    <li><strong>src/</strong>: Core MCP schema and implementation</li>
                    <li><strong>examples/</strong>: Example implementations of MCP for specific Dutch laws</li>
                  </ul>
                </div>
              </CardContent>
              <CardFooter className="flex justify-center p-0">
                <a href="https://github.com/user/dutch-law-mcp" target="_blank" rel="noopener noreferrer" className="w-full">
                  <Button className="w-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center gap-2">
                    <GithubIcon className="h-5 w-5" />
                    View on GitHub
                  </Button>
                </a>
              </CardFooter>
            </Card>
            
            <Card className="border border-slate-200 rounded-lg p-6 bg-white">
              <CardContent className="p-0">
                <h2 className="text-2xl font-semibold text-slate-800 mb-4">How to Use</h2>
                
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium text-slate-800">Clone the Repository</h3>
                    <div className="bg-slate-900 text-slate-300 p-3 rounded-md font-mono text-sm mt-2 overflow-x-auto">
                      git clone https://github.com/user/dutch-law-mcp.git
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">Explore Examples</h3>
                    <div className="bg-slate-900 text-slate-300 p-3 rounded-md font-mono text-sm mt-2 overflow-x-auto">
                      cd dutch-law-mcp/examples
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">Read Documentation</h3>
                    <p className="text-slate-600 mt-2">
                      Browse the docs/ directory to learn more about the MCP structure and how to contribute.
                    </p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">Fork for Your Own Project</h3>
                    <p className="text-slate-600 mt-2">
                      Create your own fork to start implementing MCPs for specific laws or to contribute improvements.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Repository;
