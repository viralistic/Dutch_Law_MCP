
import {
  BookOpen,
  Code2,
  FileText,
  History,
  LayoutGrid,
  Lightbulb,
  MapPin,
  Palette
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";

const features = [
  {
    icon: <FileText className="h-8 w-8 text-blue-500" />,
    title: "Identification & Basic Data",
    description: "Essential metadata about the law for better categorization and reference."
  },
  {
    icon: <History className="h-8 w-8 text-blue-500" />,
    title: "Historical Context",
    description: "Origin and development of the law to understand its purpose and evolution."
  },
  {
    icon: <LayoutGrid className="h-8 w-8 text-blue-500" />,
    title: "Content Mapping",
    description: "Structural and semantic analysis for clear understanding of the legal framework."
  },
  {
    icon: <BookOpen className="h-8 w-8 text-blue-500" />,
    title: "Interpretative Context",
    description: "Case law and legal doctrine that shapes the application of legislation."
  },
  {
    icon: <MapPin className="h-8 w-8 text-blue-500" />,
    title: "Practical Application",
    description: "Implementation and societal impact of the legislation in real-world scenarios."
  },
  {
    icon: <Code2 className="h-8 w-8 text-blue-500" />,
    title: "Digital Integration",
    description: "Technical specifications for digital access and machine readability."
  },
  {
    icon: <Lightbulb className="h-8 w-8 text-blue-500" />,
    title: "Future Perspective",
    description: "Planned developments and challenges for the evolution of the legal framework."
  },
  {
    icon: <Palette className="h-8 w-8 text-blue-500" />,
    title: "Accessibility",
    description: "Linguistic aspects and inclusivity to make law accessible to everyone."
  }
];

const Features = () => {
  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-slate-800 mb-4">MCP Components</h2>
          <p className="text-slate-600 max-w-2xl mx-auto">
            The Modern Context Protocol consists of eight main sections that provide comprehensive context for understanding Dutch law.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="border border-slate-200 rounded-lg hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="mb-2">{feature.icon}</div>
                <CardTitle className="text-slate-800">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
