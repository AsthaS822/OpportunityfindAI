export const Footer = () => {
  return (
    <footer className="bg-[#0F172A] border-t border-gray-800/50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold bg-gradient-to-r from-[#FF7A00] to-[#FF9A3D] bg-clip-text text-transparent">
              FutureOS
            </span>
            <span className="text-gray-500 text-sm">AI Decision Intelligence</span>
          </div>
          <p className="text-gray-500 text-sm">
            Empowering your future with AI-driven insights
          </p>
        </div>
      </div>
    </footer>
  );
};
