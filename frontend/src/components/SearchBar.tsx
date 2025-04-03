import { useState, useEffect, useRef } from "react";
import { MessageCircle, Send } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

interface AnalysisResult {
  categories: string[];
  laws: string[];
  advice: string;
  references: {
    name_of_law: string;
    citation_title: string;
    identification_number: string;
    legal_domain: string;
    date_of_entry_into_force: string;
    regulatory_authority: string;
  }[];
}

const commonQuestions = [
  "What is the Dutch Civil Code?",
  "How do I find specific legislation?",
  "What are my rights as a tenant in the Netherlands?",
  "How do I start a legal procedure in the Netherlands?",
  "What is the Modern Context Protocol?"
];

const SearchBar = () => {
  const [isQuestionsOpen, setIsQuestionsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const searchContainerRef = useRef<HTMLDivElement>(null);
  
  // Create glowing border effect
  useEffect(() => {
    if (!searchContainerRef.current) return;
    
    let position = 0;
    const borderLength = 2 * (searchContainerRef.current.offsetWidth + searchContainerRef.current.offsetHeight);
    
    const animateBorder = () => {
      if (!searchContainerRef.current) return;
      
      position = (position + 2) % borderLength;
      const gradientPosition = (position / borderLength) * 100;
      
      searchContainerRef.current.style.background = `
        linear-gradient(90deg, 
          rgba(194, 212, 219, 0.6) 0%, 
          rgba(231, 240, 245, 0.8) 100%)
      `;
      
      searchContainerRef.current.style.boxShadow = `0 0 0 2px rgba(22, 26, 51, 0.1)`;
      
      searchContainerRef.current.style.setProperty(
        '--border-position', 
        `${gradientPosition}%`
      );
      
      requestAnimationFrame(animateBorder);
    };
    
    const animationId = requestAnimationFrame(animateBorder);
    return () => cancelAnimationFrame(animationId);
  }, []);
  
  const handleQuestionClick = (question: string) => {
    setSearchQuery(question);
    setIsQuestionsOpen(false);
    handleSubmit(question);
  };
  
  const handleSubmit = async (questionText?: string) => {
    const query = questionText || searchQuery;
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8080/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ situation: query }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to analyze the legal situation');
      }
      
      const data = await response.json();
      if (data.success) {
        setResult(data.data);
      } else {
        setError(data.error || 'Failed to analyze the legal situation');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSubmit();
  };
  
  return (
    <div className="w-full max-w-3xl mx-auto px-4 py-6 relative">
      <div 
        ref={searchContainerRef}
        className="search-container relative"
      >
        {/* Glowing border element */}
        <div className="absolute inset-0 -z-10 rounded-[30px] overflow-hidden">
          <div 
            className="absolute inset-0 glow-border"
            style={{
              background: `
                linear-gradient(
                  90deg,
                  transparent 0%,
                  #DC1616 var(--border-position, 50%),
                  transparent 100%
                )
              `,
              filter: 'blur(8px)',
              opacity: 0.7,
              transform: 'scale(1.05)',
              borderRadius: '30px'
            }}
          />
        </div>
        
        <form onSubmit={handleFormSubmit} className="flex items-center p-2 pl-4">
          <Input
            type="text"
            placeholder="Ask me anything about Dutch law..."
            className="search-input border-none focus-visible:ring-0 focus-visible:ring-offset-0 text-[#161A33] placeholder:text-[#161A33]/60"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onFocus={() => setIsQuestionsOpen(true)}
            disabled={isLoading}
          />
          <Button 
            type="submit" 
            size="icon"
            className="ml-2 bg-[#161A33] hover:bg-[#2D3252]"
            disabled={isLoading}
          >
            <Send size={18} className="text-white" />
          </Button>
        </form>
      </div>
      
      {/* Common questions dropdown */}
      {isQuestionsOpen && (
        <div className="common-questions mt-2 bg-[#E7F0F5] rounded-lg shadow-md overflow-y-auto z-20 relative">
          <div className="p-2 border-b border-[#C2D4DB]">
            <h3 className="text-sm font-medium text-[#161A33]">Common Questions</h3>
          </div>
          <ul>
            {commonQuestions.map((question, index) => (
              <li 
                key={index}
                className="question-item px-4 py-2 cursor-pointer flex items-center gap-2 text-[#161A33] hover:bg-[#C2D4DB]/20"
                onClick={() => handleQuestionClick(question)}
              >
                <MessageCircle size={16} className="text-[#161A33]/70" />
                <span>{question}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {/* Results section */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
          {error}
        </div>
      )}
      
      {result && !error && (
        <div className="mt-4 space-y-4">
          {/* Categories */}
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="font-medium text-lg mb-2">Relevant Categories</h3>
            <div className="flex flex-wrap gap-2">
              {result.categories.map((category, index) => (
                <span key={index} className="px-3 py-1 bg-[#E7F0F5] text-[#161A33] rounded-full text-sm">
                  {category}
                </span>
              ))}
            </div>
          </div>
          
          {/* Laws */}
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="font-medium text-lg mb-2">Relevant Laws</h3>
            <ul className="list-disc list-inside space-y-1">
              {result.laws.map((law, index) => (
                <li key={index} className="text-[#161A33]">{law}</li>
              ))}
            </ul>
          </div>
          
          {/* Advice */}
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="font-medium text-lg mb-2">Legal Advice</h3>
            <p className="text-[#161A33] whitespace-pre-wrap">{result.advice}</p>
          </div>
          
          {/* References */}
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="font-medium text-lg mb-2">References</h3>
            <div className="space-y-3">
              {result.references.map((ref, index) => (
                <div key={index} className="border-l-2 border-[#C2D4DB] pl-3">
                  <h4 className="font-medium">{ref.name_of_law}</h4>
                  <p className="text-sm text-[#161A33]/70">{ref.citation_title}</p>
                  <p className="text-sm text-[#161A33]/70">BWB ID: {ref.identification_number}</p>
                  <p className="text-sm text-[#161A33]/70">Domain: {ref.legal_domain}</p>
                  <p className="text-sm text-[#161A33]/70">Entry into force: {ref.date_of_entry_into_force}</p>
                  <p className="text-sm text-[#161A33]/70">Authority: {ref.regulatory_authority}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
