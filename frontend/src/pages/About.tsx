
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card, CardContent } from "@/components/ui/card";

const About = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow py-16 bg-slate-50">
        <div className="container mx-auto px-6">
          <div className="max-w-3xl mx-auto">
            <h1 className="text-4xl font-bold text-slate-800 mb-10">About Dutch Law MCP</h1>
            
            <Card className="border border-slate-200 rounded-lg p-6 bg-white mb-8">
              <CardContent className="p-0">
                <h2 className="text-2xl font-semibold text-slate-800 mb-4">Mission</h2>
                <p className="text-slate-600 mb-6">
                  Our mission is to democratize access to legal knowledge by creating a standardized framework that makes Dutch law more accessible, comprehensible, and usable for everyone – from legal professionals to everyday citizens and even AI systems.
                </p>
                <p className="text-slate-600">
                  We believe that understanding the law shouldn't be a privilege for the few. By breaking down the knowledge monopoly, we aim to empower people to navigate their legal rights and obligations more effectively, ultimately achieving better outcomes in their lives.
                </p>
              </CardContent>
            </Card>
            
            <Card className="border border-slate-200 rounded-lg p-6 bg-white mb-8">
              <CardContent className="p-0">
                <h2 className="text-2xl font-semibold text-slate-800 mb-4">What Makes MCP Different</h2>
                <p className="text-slate-600 mb-4">
                  The Modern Context Protocol (MCP) goes beyond simply digitizing legal texts. It enriches them with:
                </p>
                <ul className="list-disc list-inside space-y-2 text-slate-600 mb-4">
                  <li>Historical context to understand the law's origins</li>
                  <li>Interpretative guidance from case law and doctrine</li>
                  <li>Practical application examples</li>
                  <li>Future perspectives on legal developments</li>
                  <li>Accessibility considerations for diverse users</li>
                </ul>
                <p className="text-slate-600">
                  This comprehensive approach ensures that users not only access the letter of the law but truly understand its meaning and application in real-world contexts.
                </p>
              </CardContent>
            </Card>
            
            <Card className="border border-slate-200 rounded-lg p-6 bg-white">
              <CardContent className="p-0">
                <h2 className="text-2xl font-semibold text-slate-800 mb-4">Open Collaboration</h2>
                <p className="text-slate-600 mb-4">
                  The Dutch Law MCP is an open project that welcomes contributions from legal experts, developers, linguists, and anyone passionate about improving legal access.
                </p>
                <p className="text-slate-600">
                  By fostering a collaborative ecosystem, we aim to continuously improve and expand the MCP framework, ensuring it remains relevant and valuable in an evolving legal landscape.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default About;
