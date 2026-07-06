import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';

import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { PageTransition } from './components/motion/PageTransition';
import { Container } from './components/layout/Container';
import { Home } from './pages/Home';
import Discovery from './pages/Discovery';

const Layout = () => (
  <div className="min-h-screen flex flex-col">
    <Navbar />
    <main className="flex-1">
      <Outlet />
    </main>
    <Footer />
  </div>
);

const PlaceholderPage = ({ title }: { title: string }) => (
  <PageTransition>
    <Container className="py-20 text-center">
      <h1 className="text-4xl font-heading font-bold">{title}</h1>
      <p className="mt-4 text-text-secondary">This page has not been built yet.</p>
    </Container>
  </PageTransition>
);

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/discover" element={<Discovery />} />
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/report" element={<PlaceholderPage title="Report" />} />
          <Route path="/opportunity/:id" element={<PlaceholderPage title="Opportunity Detail" />} />
          <Route path="/compare" element={<PlaceholderPage title="Compare" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
