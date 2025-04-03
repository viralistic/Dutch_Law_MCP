
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import AboutSection from "@/components/AboutSection";
import CreatorProfile from "@/components/CreatorProfile";
import GetStartedSection from "@/components/GetStartedSection";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Navbar />
      <main className="flex-grow">
        <Hero />
        <Features />
        <AboutSection />
        <CreatorProfile />
        <GetStartedSection />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
