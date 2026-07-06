import { motion } from 'framer-motion';

export const LoadingSkeleton = ({ className = '' }: { className?: string }) => (
  <motion.div
    className={`bg-gray-200 rounded-xl ${className}`}
    animate={{ opacity: [0.5, 1, 0.5] }}
    transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
  />
);
