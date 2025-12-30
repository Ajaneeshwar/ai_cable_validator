/**
 * Home Page - Redirects to Design Validator
 */
import { redirect } from 'next/navigation';

export default function Home() {
    redirect('/design-validator');
}
