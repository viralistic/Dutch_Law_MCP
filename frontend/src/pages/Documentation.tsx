
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card, CardContent } from "@/components/ui/card";

const Documentation = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow py-16 bg-slate-50">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-slate-800 mb-10">Documentation</h1>
            
            <Card className="border border-slate-200 rounded-lg p-6 bg-white mb-8">
              <CardContent className="p-0">
                <h2 className="text-2xl font-semibold text-slate-800 mb-4">Getting Started</h2>
                <p className="text-slate-600 mb-6">
                  To use this framework:
                </p>
                <ol className="list-decimal list-inside space-y-2 text-slate-600">
                  <li>Clone the repository from GitHub</li>
                  <li>Explore the examples/ directory to understand implementation patterns</li>
                  <li>Follow documentation in docs/ to create an MCP for a specific law</li>
                </ol>
              </CardContent>
            </Card>
            
            <Card className="border border-slate-200 rounded-lg p-6 bg-white mb-8">
              <CardContent className="p-0">
                <h2 className="text-2xl font-semibold text-slate-800 mb-4">MCP Structure</h2>
                <p className="text-slate-600 mb-4">
                  Each MCP document contains eight key sections:
                </p>
                
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium text-slate-800">1. Identification & Basic Data</h3>
                    <p className="text-slate-600">Metadata about the law including title, number, effective date, etc.</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">2. Historical Context</h3>
                    <p className="text-slate-600">Background on why the law was created, its legislative history, and amendments over time.</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">3. Content Mapping</h3>
                    <p className="text-slate-600">Breakdown of the law's structure, key concepts, and relationships between provisions.</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">4. Interpretative Context</h3>
                    <p className="text-slate-600">Notable case law, academic interpretations, and official guidance.</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">5. Practical Application</h3>
                    <p className="text-slate-600">How the law is implemented in practice, common scenarios, and societal impact.</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">6. Digital Integration</h3>
                    <p className="text-slate-600">Technical specifications for APIs, data models, and machine-readable formats.</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">7. Future Perspective</h3>
                    <p className="text-slate-600">Pending changes, policy debates, and anticipated developments.</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-slate-800">8. Accessibility</h3>
                    <p className="text-slate-600">Plain language summaries, translations, and considerations for diverse users.</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="border border-slate-200 rounded-lg p-6 bg-white">
              <CardContent className="p-0">
                <h2 className="text-2xl font-semibold text-slate-800 mb-4">Contributing</h2>
                <p className="text-slate-600 mb-4">
                  Contributions to improve the Dutch Law MCP framework are welcome. Here's how you can contribute:
                </p>
                <ul className="list-disc list-inside space-y-2 text-slate-600">
                  <li>Fork the repository and create a new branch for your feature</li>
                  <li>Make your changes following the contribution guidelines</li>
                  <li>Submit a pull request with a clear description of your changes</li>
                  <li>Participate in the review process</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Documentation;
