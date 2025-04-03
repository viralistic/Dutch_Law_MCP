
import { Card, CardContent } from "./ui/card";

const CreatorProfile = () => {
  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold text-slate-800 mb-2">About the Creator</h2>
            <p className="text-slate-600">Meet the mind behind the Dutch Law MCP</p>
          </div>
          
          <Card className="border border-slate-200 rounded-lg overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-3">
              <div className="md:col-span-1 bg-slate-50 flex items-center justify-center p-6">
                <div className="w-48 h-48 rounded-full overflow-hidden border-4 border-white shadow-md">
                  <img 
                    src="/lovable-uploads/4c6b0fe1-7cdd-4431-b256-c29f7f9a6941.png" 
                    alt="Marrallisa Kreijkes" 
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
              
              <div className="md:col-span-2 p-8">
                <CardContent className="p-0">
                  <h3 className="text-2xl font-bold text-slate-800 mb-2">Marrallisa Kreijkes</h3>
                  <p className="text-blue-500 mb-4">Legal Innovation Specialist</p>
                  
                  <p className="text-slate-600 mb-6">
                    Passionate about democratizing access to legal knowledge through technology. 
                    I created the Dutch Law MCP to bridge the gap between complex legal texts and everyday understanding,
                    enabling both individuals and AI systems to better navigate Dutch legislation.
                  </p>
                  
                  <div className="flex flex-wrap gap-4 mt-4">
                    <a 
                      href="https://viralistic.nl" 
                      target="_blank"
                      rel="noopener noreferrer" 
                      className="text-blue-500 hover:text-blue-700 flex items-center gap-1"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                        <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                      </svg>
                      viralistic.nl
                    </a>
                    <a 
                      href="https://t.me/vrlstc" 
                      target="_blank"
                      rel="noopener noreferrer" 
                      className="text-blue-500 hover:text-blue-700 flex items-center gap-1"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="m22 2-7 20-4-9-9-4Z"></path>
                        <path d="M22 2 11 13"></path>
                      </svg>
                      @vrlstc
                    </a>
                  </div>
                </CardContent>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default CreatorProfile;
