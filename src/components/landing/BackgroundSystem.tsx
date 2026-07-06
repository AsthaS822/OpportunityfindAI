import { motion } from 'framer-motion';

export const BackgroundSystem = () => {
  return (
    <div className="fixed inset-0 z-[-1] overflow-hidden pointer-events-none opacity-40">
      {/* Soft mesh gradient base */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-orange-50/40 via-white to-blue-50/30" />
      
      {/* Light Blobs */}
      <motion.div 
        animate={{
          x: [0, 100, -50, 0],
          y: [0, -50, 100, 0],
        }}
        transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
        className="absolute top-[10%] left-[20%] w-[600px] h-[600px] bg-primary/5 rounded-full blur-[100px]"
      />
      <motion.div 
        animate={{
          x: [0, -100, 50, 0],
          y: [0, 100, -50, 0],
        }}
        transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
        className="absolute top-[40%] right-[10%] w-[500px] h-[500px] bg-secondary/5 rounded-full blur-[100px]"
      />
      <motion.div 
        animate={{
          x: [0, 50, -100, 0],
          y: [0, 50, -50, 0],
        }}
        transition={{ duration: 35, repeat: Infinity, ease: "linear" }}
        className="absolute bottom-[10%] left-[30%] w-[700px] h-[700px] bg-accent/5 rounded-full blur-[120px]"
      />
      
      {/* Subtle Noise Texture */}
      <div 
        className="absolute inset-0 opacity-[0.015] mix-blend-overlay"
        style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=%220 0 200 200%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noiseFilter%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.65%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noiseFilter)%22/%3E%3C/svg%3E")' }}
      />
    </div>
  );
};
