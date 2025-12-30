/**
 * Root Layout Component
 */
import { Metadata } from 'next';
import ThemeProvider from '@/theme/ThemeProvider';

export const metadata: Metadata = {
    title: 'Cable Design Validator | InnoVites',
    description: 'AI-Driven Cable Design Validation System for IEC Standards Compliance',
    keywords: ['cable design', 'IEC 60502-1', 'IEC 60228', 'validation', 'AI', 'InnoVites'],
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
                <link
                    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
                    rel="stylesheet"
                />
            </head>
            <body>
                <ThemeProvider>
                    {children}
                </ThemeProvider>
            </body>
        </html>
    );
}
