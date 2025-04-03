
import { Card, CardContent } from "./ui/card";

const AboutSection = () => {
  return (
    <section className="py-16 bg-slate-50">
      <div className="container mx-auto px-6">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-slate-800 mb-6 text-center">About Dutch Law MCP</h2>
          
          <Card className="border border-slate-200 rounded-lg p-6 bg-white mb-8">
            <CardContent className="p-0">
              <h3 className="text-xl font-semibold text-slate-800 mb-4">What is MCP?</h3>
              <p className="text-slate-600 mb-4">
                The Modern Context Protocol (MCP) is a standardized method for enriching legal texts with contextual information, making them more accessible, comprehensible, and usable for various audiences, from legal professionals to AI systems.
              </p>
              <p className="text-slate-600">
                This project aims to democratize access to Dutch legal knowledge, ensuring that everyone has equal opportunity to understand and apply the law, without being limited by knowledge monopolies.
              </p>
            </CardContent>
          </Card>
          
          <Card className="border border-slate-200 rounded-lg p-6 bg-white">
            <CardContent className="p-0">
              <h3 className="text-xl font-semibold text-slate-800 mb-4">Repository Structure</h3>
              <ul className="list-disc list-inside space-y-2 text-slate-600">
                <li><strong>docs/</strong>: Documentation on how to use and contribute to the MCP framework</li>
                <li><strong>src/</strong>: Core MCP schema and implementation</li>
                <li><strong>examples/</strong>: Example implementations of MCP for specific Dutch laws</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
