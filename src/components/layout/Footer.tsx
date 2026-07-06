import { Container } from './Container';
import { useTranslation } from 'react-i18next';

export const Footer = () => {
  const { t } = useTranslation();
  
  return (
    <footer className="border-t border-border bg-background py-12 text-center text-text-secondary">
      <Container>
        <p>{t('footer.rights')}</p>
      </Container>
    </footer>
  );
};
